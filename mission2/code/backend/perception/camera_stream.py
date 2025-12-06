import cv2
import threading
import time
import logging

class CameraStream:
    def __init__(self, src=0):
        self.src = src
        self.stream = cv2.VideoCapture(self.src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False
        self.logger = logging.getLogger("CameraStream")

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
            
            with threading.Lock(): # Minimal lock just to swap reference
                self.grabbed = grabbed
                self.frame = frame
            
            time.sleep(0.01) # Small sleep to preventing hogging CPU

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        if self.t.is_alive():
            self.t.join()
        self.stream.release()
