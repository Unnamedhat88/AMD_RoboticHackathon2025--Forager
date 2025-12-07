class PoseEstimator:
    def __init__(self, frame_width=640, frame_height=480):
        self.frame_width = frame_width
        self.frame_height = frame_height
        # Default fixed depth for now (Phase 2.F)
        self.default_z = 0.35 

    def estimate_pose(self, box):
        """
        Estimate 3D grasp pose from 2D bounding box.
        Returns: {'x': float, 'y': float, 'z': float, 'roll': 0, 'pitch': 0, 'yaw': 0}
        """
        # box is [xmin, ymin, xmax, ymax]
        xmin, ymin, xmax, ymax = box
        
        # Calculate center in 2D
        cx = (xmin + xmax) / 2
        cy = (ymin + ymax) / 2
        
        # Normalize to -1.0 to 1.0 (0,0 is center of frame)
        # x: -1 (left) to 1 (right)
        # y: -1 (top) to 1 (bottom) — typically robot coord system might have different Y/Z
        # For this simple heuristic:
        # X robot = map pixel X to physical range (e.g. -0.2m to 0.2m)
        # Y robot = map pixel Y to physical range (e.g. 0.3m to 0.5m)
        
        # Simple linear mapping for Hackathon demo
        # Assuming camera is mounted facing workspace
        
        norm_x = (cx - self.frame_width / 2) / (self.frame_width / 2)
        norm_y = (cy - self.frame_height / 2) / (self.frame_height / 2)
        
        # Physical workspace estimation (in meters)
        # Arbitrary scaling factors for the demo
        est_x = norm_x * 0.2  # +/- 20cm width
        est_y = 0.4 + (norm_y * 0.1) # 40cm depth +/- 10cm
        
        return {
            "x": float(round(est_x, 3)),
            "y": float(round(est_y, 3)),
            "z": float(self.default_z),
            "roll": 0.0,
            "pitch": -1.57, # Pointing down (roughly -90 deg)
            "yaw": 0.0
        }
