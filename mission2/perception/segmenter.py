import numpy as np
import torch

class GrocerySegmenter:
    def __init__(self, device=None):
        # In a real scenario, load SAM model here
        # self.sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        print(f"GrocerySegmenter initialized on {self.device} (Mock Mode for now)")

    def segment_objects(self, image, boxes):
        """
        Generates masks for given bounding boxes.
        
        Args:
            image: numpy array
            boxes: list of [xmin, ymin, xmax, ymax]
            
        Returns:
            list of masks (numpy bool arrays)
        """
        masks = []
        h, w = image.shape[:2]
        
        for box in boxes:
            xmin, ymin, xmax, ymax = map(int, box)
            mask = np.zeros((h, w), dtype=bool)
            # Create a simple rectangular mask for the box
            mask[ymin:ymax, xmin:xmax] = True
            masks.append(mask)
            
        return masks
