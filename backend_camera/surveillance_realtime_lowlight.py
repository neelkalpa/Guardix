import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
    """Adjust image gamma for brightness correction"""
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                     for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

# Initialize video capture
cap = cv2.VideoCapture(1)

# Load face detection classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()
    
if face_cascade.empty():
    print("Error loading face detection model.")
    exit()

# Set camera properties for low light
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cap.set(cv2.CAP_PROP_EXPOSURE, -5)

# Create CLAHE object for contrast enhancement
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply enhancements
    gamma_corrected = adjust_gamma(gray, gamma=0.65)
    enhanced = clahe.apply(gamma_corrected)
    
    # Detect faces in the enhanced image
    faces = face_cascade.detectMultiScale(
        enhanced,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Convert enhanced image to BGR for color annotations
    display_frame = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
    
    # Draw red rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(display_frame, 
                     (x, y), 
                     (x + w, y + h), 
                     (0, 0, 255),  # Red color in BGR format
                     2)             # Line thickness
    
    # Display the result
    cv2.imshow('Low Light B/W Camera with Face Detection', display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()