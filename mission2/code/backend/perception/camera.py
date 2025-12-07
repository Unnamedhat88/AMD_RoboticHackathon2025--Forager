import cv2
import numpy as np
import time

class CameraInterface:
    def __init__(self, device_id="/dev/video2", mock=True):
        self.mock = mock
        self.device_id = device_id
        if not self.mock:
            self.cap = cv2.VideoCapture(device_id)
        
    def get_frame(self):
        """Returns a frame from the camera."""
        if self.mock:
            # Return a generated image (noise or static pattern)
            height, width = 480, 640
            # diverse colors for testing
            img = np.zeros((height, width, 3), np.uint8)
            cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), -1) # Green box
            cv2.circle(img, (400, 300), 50, (0, 0, 255), -1) # Red circle
            # Add timestamp text
            cv2.putText(img, f"Mock Frame {time.time()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return img
        else:
            ret, frame = self.cap.read()
            if not ret:
                # Try to reconnect or just log error? For now raise.
                # In robust system we might want to release and re-open.
                raise RuntimeError("Failed to capture frame from Camera")
            return frame

    def capture_frame(self):
        """Alias for get_frame to match spec."""
        return self.get_frame()

    def release(self):
        if not self.mock:
            self.cap.release()
