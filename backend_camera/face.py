from base64 import b64decode
from io import BytesIO
import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import ssl
import os
import cv2

ssl._create_default_https_context = ssl._create_unverified_context
model_path = 'models/inception_resnet_v1_vggface2.pth'
mtcnn = MTCNN(keep_all=False)

if not os.path.exists('models'):
    os.makedirs('models')

if not os.path.exists(model_path):
    model = InceptionResnetV1(pretrained='vggface2').eval()
    torch.save(model.state_dict(), model_path)
else:    
    model = InceptionResnetV1(pretrained=None).eval()    
    model.load_state_dict(torch.load(model_path), strict=False)

def get_face_embedding_base64(image_str):
    image_data = b64decode(image_str)
    img = Image.open(BytesIO(image_data))

    face = mtcnn(img)

    if face is not None:
        face = face.unsqueeze(0)
        with torch.no_grad():
            embedding = model(face)
        return embedding
    else:
        return None

def matchFace(image1, image2): 

    embedding1 = get_face_embedding_base64(image1)
    embedding2 = get_face_embedding_base64(image2)

    if embedding1 is None or embedding2 is None:
        return False

    cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
    similarity = cos(embedding1, embedding2)

    return similarity.item() > 0.6

#! Test the function
"""
import base64

def read_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

a = read_image_as_base64("saved_faces/2.jpg")
b = read_image_as_base64("saved_faces/3.jpg")

print(matchFace(a, b))
"""