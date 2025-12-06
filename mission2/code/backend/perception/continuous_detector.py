import threading
import time
import logging
from ultralytics import YOLO

class PerceptionLoop:
    def __init__(self, camera_stream, tracker_state, model_path="yolov8n.pt"):
        self.camera_stream = camera_stream
        self.tracker_state = tracker_state
        self.stopped = False
        self.logger = logging.getLogger("PerceptionLoop")
        
        self.logger.info(f"Loading YOLO model {model_path}...")
        try:
            self.model = YOLO(model_path)
            # Warmup
            # self.model.track(source=self.camera_stream.read(), persist=True, tracker="bytetrack.yaml", verbose=False) 
            self.logger.info("Model loaded.")
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
        Map YOLOv8 COCO labels to Grocery labels.
        """
        mapping = {
            "banana": "Banana",
            "apple": "Red Apple",
            "orange": "Orange",
            "broccoli": "Broccoli",
            "carrot": "Carrot",
            "bottle": "Milk", 
            "cup": "Cereal",
            "box": "Cereal",
        }
        return mapping.get(label, label.title())

    def stop(self):
        self.stopped = True
        if self.t.is_alive():
            self.t.join()
