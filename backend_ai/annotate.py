import cv2
from ultralytics import YOLO

def detect_objects_in_image(image_path, output_path='annotated.jpg'):

    model = YOLO('yolov8n.pt')  

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    results = model(image)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = round(box.conf[0].item(), 2)
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Label text
            label = f"{class_name}: {confidence}"
            (text_width, text_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

            # Label background
            cv2.rectangle(image, 
                          (x1, y1 - text_height - 10),
                          (x1 + text_width, y1 - 10),
                          (0, 255, 0), -1)

            # Label text
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Save or show the result
    cv2.imshow('Detected Objects', image)
    cv2.imwrite(output_path, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
detect_objects_in_image('crossing.jpg')
#         