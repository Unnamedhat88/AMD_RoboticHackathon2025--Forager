import torch
from ultralytics import YOLO
import numpy as np

class GroceryDetector:
    def __init__(self, model_path="yolov8n.pt", device=None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Loading YOLOv8 model ({model_path}) on {self.device}...")
        try:
            self.model = YOLO(model_path)
            # Warmup
            # self.model(np.zeros((640, 640, 3), dtype=np.uint8)) 
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def detect_item(self, image):
        """
        Detects the most prominent item in the image for /scan endpoint.
        Returns mapped label and confidence.
        """
        if self.model is None:
            return {"name": "Unknown (Model Failed)", "confidence": 0.0}

        # Run inference
        results = self.model(image, verbose=False)
        
        # Process results
        # We want the highest confidence object
        best_box = None
        best_conf = -1.0
        best_class_id = -1
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                conf = float(box.conf)
                if conf > best_conf:
                    best_conf = conf
                    best_box = box.xyxy[0].tolist() # [xmin, ymin, xmax, ymax]
                    best_class_id = int(box.cls)
        
        if best_conf < 0.3: # Threshold
             return {"name": "Unknown Item", "confidence": 0.0}
             
        # Get label map
        raw_label = self.model.names[best_class_id]
        clean_label = self._map_label(raw_label)
        
        return {
            "name": clean_label,
            "confidence": best_conf,
            "box": best_box # Optional: might be useful later
        }

    def _map_label(self, label):
        """
        Map YOLOv8 COCO labels to Grocery labels.
        COCO classes relevant: 'banana', 'apple', 'orange', 'broccoli', 'carrot', 'bottle', 'cup' ...
        """
        mapping = {
            "banana": "Banana",
            "apple": "Red Apple",
            "orange": "Orange",
            "broccoli": "Broccoli",
            "carrot": "Carrot",
            "bottle": "Milk", # Assuming bottle -> Milk for now based on prompt
            "cup": "Cereal", # Weird mapping but placeholders
            "box": "Cereal", # Not in COCO usually, but maybe YOLO defines it?
        }
        return mapping.get(label, label.title())

if __name__ == "__main__":
    det = GroceryDetector()
    # Mock image test
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    print(det.detect_item(img))
