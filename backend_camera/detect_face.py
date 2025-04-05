import cv2

def detect_faces(image_path, output_path='output.jpg'):
    # Load pre-trained Haar Cascade
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    if face_cascade.empty():
        raise FileNotFoundError("Haar cascade XML file not found. Ensure OpenCV is installed correctly.")
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image file")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )
    
    # Draw larger circles around faces
    for (x, y, w, h) in faces:
        center = (x + w//2, y + h//2)
        # Increase radius by using 70% of the maximum dimension
        radius = int(round(max(w, h) * 1.0))  # Changed from (w+h)/4
        cv2.circle(img, center, radius, (0, 255, 0), 3)
    
    cv2.imwrite(output_path, img)
    return len(faces) > 0

print(detect_faces('saved_faces/5.jpg', 'output.jpg'))
print(detect_faces('saved_faces/4.jpg', 'output.jpg'))