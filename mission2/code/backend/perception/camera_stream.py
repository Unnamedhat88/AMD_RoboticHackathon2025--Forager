import cv2
import threading
import time
import logging

class CameraStream:
    def __init__(self, src=0):
        self.src = src
        self.stream = cv2.VideoCapture(self.src)
        
        # Camera Settings
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Increase Brightness/Contrast/Exposure (Hardware)
        # Values range depends on camera, but often 0-1 or specific range.
        # Trying common values for V4L2 backend
        self.stream.set(cv2.CAP_PROP_BRIGHTNESS, 0.7) # 0.0 - 1.0 (or camera specific)
        self.stream.set(cv2.CAP_PROP_CONTRAST, 0.6)
        # self.stream.set(cv2.CAP_PROP_EXPOSURE, -4) # Auto-exposure is usually better if lighting varies
        
        self.grabbed, self.frame = self.stream.read()
        
        # Apply initial software boost if hardware fails to brighten enough
        if self.grabbed and self.frame.mean() < 50:
            self.logger.warning("Camera image extremely dark, checking auto-exposure...")

        self.stopped = False
        self.logger = logging.getLogger("CameraStream")
        self.lock = threading.Lock()

        if not self.grabbed:
            self.logger.error("Failed to open camera source")
            self.stopped = True

    def start(self):
        self.t = threading.Thread(target=self.update, args=())
        self.t.daemon = True
        self.t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            
            grabbed, frame = self.stream.read()
            if not grabbed:
                self.logger.warning("Camera read failed, retrying...")
                time.sleep(0.1)
                continue
            
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame
            
            time.sleep(0.01) # Small sleep to preventing hogging CPU

    def read(self):
        with self.lock:
            # Software Brightness/Gamma Correction
            # Gamma < 1.0 makes dark regions lighter
            if self.frame is not None:
                # Optimized gamma correction using LUT
                import numpy as np
                gamma = 0.6 # < 1.0 to brighten
                invGamma = 1.0 / gamma
                table = np.array([((i / 255.0) ** invGamma) * 255
                    for i in np.arange(0, 256)]).astype("uint8")
                return cv2.LUT(self.frame, table)
            return self.frame

    def stop(self):
        self.stopped = True
        if self.t.is_alive():
            self.t.join()
        self.stream.release()
