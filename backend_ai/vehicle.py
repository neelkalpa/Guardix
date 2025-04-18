from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration, BitsAndBytesConfig
from PIL import Image
import torch


quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
)

model_id = "llava-hf/llava-v1.6-mistral-7b-hf"
device = "cuda" if torch.cuda.is_available() else "mps"

# Fix 2: Use LlavaNext classes instead of Llava
processor = LlavaNextProcessor.from_pretrained(model_id, cache_dir="cache")
model = LlavaNextForConditionalGeneration.from_pretrained(
    model_id,
    quantization_config=quantization_config,
    device_map="auto",
    torch_dtype=torch.float16,
    cache_dir="cache"
)

# Fix 3: Explicit input formatting
image = Image.open("vehicle.jpg")
prompt = "USER: <image>\nAnswer 'True' if you see a vehicle. Else answer 'False'. Answer in one word only\nASSISTANT:"

# Fix 4: Proper input processing with both text and images
inputs = processor(
    text=prompt, 
    images=image, 
    return_tensors="pt", 
    padding=True
).to(device)

# Fix 5: Add generation parameters
output = model.generate(
    **inputs,
    max_new_tokens=2,

    temperature=0.7
)

description = processor.decode(output[0], skip_special_tokens=True)
print(description.split("ASSISTANT: ")[-1])