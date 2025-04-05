import cv2

# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture
cap = cv2.VideoCapture(1)  # Change to 0 if using the default camera
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for both processing and thermal effect
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Create thermal effect
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # Draw white rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(heatmap, (x, y), (x+w, y+h), (255, 255, 255), 2)

    # Display result
    cv2.imshow('Thermal Camera with Face Detection', heatmap)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()