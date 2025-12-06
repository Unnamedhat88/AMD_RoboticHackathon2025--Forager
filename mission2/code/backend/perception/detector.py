import torch
from transformers import pipeline
from PIL import Image
import numpy as np

class GroceryDetector:
    def __init__(self, model_id="IDEA-Research/grounding-dino-tiny", device=None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        print(f"Loading GroundingDINO model ({model_id}) on {self.device}...")
        try:
            # Use zero-shot-object-detection pipeline
            self.detector = pipeline("zero-shot-object-detection", model=model_id, device=self.device)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.detector = None

    def detect_objects(self, image, text_prompts):
        """
        Detects objects in an image based on text prompts.
        
        Args:
            image: numpy array (H, W, 3) or PIL Image.
            text_prompts: List of strings (e.g. ["apple", "banana"])
        
        Returns:
            list of dicts: [{'score': float, 'label': str, 'box': [xmin, ymin, xmax, ymax]}]
        """
        if self.detector is None:
            print("Detector not initialized.")
            return []

        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # zero-shot-object-detection pipeline expects 'candidate_labels' as a list of strings
        if isinstance(text_prompts, str):
            text_prompts = [text_prompts]

        # Run detection
        # The pipeline returns a list of dicts: {'score': float, 'label': str, 'box': {'xmin': int, 'ymin': int, 'xmax': int, 'ymax': int}}
        try:
            results = self.detector(image, candidate_labels=text_prompts)
        except Exception as e:
            print(f"Error during detection: {e}")
            return []
        
        # Format results
        formatted_results = []
        for r in results:
            box = r['box']
            # Ensure box is in [xmin, ymin, xmax, ymax] list format
            fmt_box = [box['xmin'], box['ymin'], box['xmax'], box['ymax']]
            formatted_results.append({
                'score': r['score'],
                'label': r['label'],
                'box': fmt_box
            })
            
        return formatted_results

    def detect_item(self, image):
        """
        Mock detection for Phase 1.A.
        Returns a random item from the grocery list.
        """
        import random
        GROCERY_CLASSES = ["apple", "banana", "bread", "milk", "egg"]
        
        # Simulate processing time
        # import time
        # time.sleep(0.5)
        
        item = random.choice(GROCERY_CLASSES)
        confidence = random.uniform(0.8, 0.99)
        
        return {
            "label": item,
            "score": confidence,
            "box": [100, 100, 200, 200] # Dummy box
        }

if __name__ == "__main__":
    # Test block
    det = GroceryDetector()
    img = Image.new('RGB', (640, 480), color='white')
    res = det.detect_objects(img, ["apple", "banana"])
    print(res)
