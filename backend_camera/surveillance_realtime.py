import cv2
import datetime
import time

def face_detection():
    cap = cv2.VideoCapture(1)  
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    scale_factor = 1.1
    min_neighbors = 5
    min_size = (30, 30)

    cooldown = 2
    last_capture = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=scale_factor,
                minNeighbors=min_neighbors,
                minSize=min_size
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                cv2.putText(frame, 'Face Detected', (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


            cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Stopping surveillance...")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_detection()
