import cv2
from ultralytics import YOLO

def normal_camera():

    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')  # Fastest version for real-time

    # Initialize webcam (1 is the camera index, change if needed)
    cap = cv2.VideoCapture(1)

    # Check if webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam. Check if camera index is correct and permissions.")

    while cap.isOpened():
        # Read frame from webcam
        success, frame = cap.read()
        
        if not success:
            print("Failed to capture frame")
            break

        # Perform object detection
        results = model(frame, verbose=False)  # verbose=False to reduce output
        
        # Process detections
        for result in results:
            for box in result.boxes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                
                # Get confidence score
                confidence = round(box.conf[0].item(), 2)
                
                # Get class name
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                
                # Draw green bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Create label text
                label = f"{class_name}: {confidence}"
                
                # Calculate text size
                (text_width, text_height), _ = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                
                # Draw label background
                cv2.rectangle(frame, 
                            (x1, y1 - text_height - 10),
                            (x1 + text_width, y1 - 10),
                            (0, 255, 0), -1)
                
                # Put confidence text
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # Display processed frame
        cv2.imshow('Real-time Object Detection', frame)
        
        # Break loop with 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

