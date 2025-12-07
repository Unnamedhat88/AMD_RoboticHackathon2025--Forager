import threading
import time
import logging
from ultralytics import YOLOWorld

class PerceptionLoop:
    def __init__(self, camera_stream, tracker_state, model_path="yolov8s-world.pt"):
        self.camera_stream = camera_stream
        self.tracker_state = tracker_state
        self.stopped = False
        self.logger = logging.getLogger("PerceptionLoop")
        
        self.logger.info(f"Loading YOLO-World model {model_path}...")
        try:
            self.model = YOLOWorld(model_path)
            # Set custom classes for the demo
            self.model.set_classes(["Pocky box"])
            self.logger.info("Model loaded. Classes set to: ['Pocky box']")
        except Exception as e:
            self.logger.error(f"Failed to load YOLO model: {e}")
            self.model = None

    def start(self):
        self.t = threading.Thread(target=self.run, args=())
        self.t.daemon = True
        self.t.start()
        return self

    def run(self):
        self.logger.info("Starting perception loop...")
        while not self.stopped:
            frame = self.camera_stream.read()
            if frame is None:
                time.sleep(0.1)
                continue
            
            if self.model:
                try:
                    # Run tracking
                    # persist=True is crucial for tracking
                    results = self.model.track(source=frame, persist=True, tracker="bytetrack.yaml", verbose=False)
                    
                    # Update state
                    for r in results:
                        if r.boxes and r.boxes.id is not None:
                            ids = r.boxes.id.cpu().numpy().astype(int)
                            clss = r.boxes.cls.cpu().numpy().astype(int)
                            confs = r.boxes.conf.cpu().numpy()
                            boxes = r.boxes.xyxy.cpu().numpy()
                            
                            for i, track_id in enumerate(ids):
                                cls_id = clss[i]
                                conf = confs[i]
                                box = boxes[i]
                                
                                raw_label = self.model.names[cls_id]
                                clean_label = self._map_label(raw_label)
                                
                                # Filter low confidence
                                if conf > 0.4: 
                                    self.tracker_state.update(track_id, clean_label, conf, box)
                                    
                except Exception as e:
                    self.logger.error(f"Error in tracking loop: {e}")
            
            # Prune old objects occasionally
            self.tracker_state.prune()
            
            # Control frame rate roughly (e.g., 20 FPS)
            time.sleep(0.05)

    def _map_label(self, label):
        """
        Map labels if needed. For YOLO-World, it should match our set classes.
        """
        return label # Pass through exactly as detected

    def stop(self):
        self.stopped = True
        if self.t.is_alive():
            self.t.join()
