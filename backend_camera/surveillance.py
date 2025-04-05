import cv2
import datetime
import time

def motion_detection():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Adjustable parameters
    min_area = 2000          # Minimum contour area to consider as motion
    var_threshold = 25       # Background subtractor sensitivity (higher = less sensitive)
    consecutive_frames = 2   # Required consecutive detection frames
    motion_counter = 0
    
    # Initialize background subtractor with configurable threshold
    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, detectShadows=False)
    back_sub.setVarThreshold(var_threshold)  # Set the variance threshold here
    back_sub.setComplexityReductionThreshold(0.05)  # Lower complexity reduction

    # Camera settings
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Disable auto-exposure
    cap.set(cv2.CAP_PROP_EXPOSURE, -6)         # Manual exposure
    
    cooldown = 2
    last_capture = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Preprocessing pipeline
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (25, 25), 0)
            
            # Background subtraction
            fg_mask = back_sub.apply(gray)
            
            # Noise reduction
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)
            
            # Contour detection
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > min_area:
                    motion_detected = True
                    break

            # Validation system
            if motion_detected:
                motion_counter += 1
                if motion_counter >= consecutive_frames:
                    current_time = time.time()
                    if current_time - last_capture > cooldown:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"motion/motion_{timestamp}.jpg"
                        cv2.imwrite(filename, frame)
                        print(f"Confirmed motion! Saved {filename}")
                        last_capture = current_time
                        motion_counter = 0
            else:
                motion_counter = 0

            # Debug views (uncomment to visualize)
            # cv2.imshow('Motion Mask', fg_mask)
            # cv2.imshow('Camera Feed', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Stopping surveillance...")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    motion_detection()