import numpy as np
import logging

class GraspPlanner:
    def __init__(self, camera_matrix=None):
        # intrinsic matrix K
        # fx 0 cx
        # 0 fy cy
        # 0 0  1
        if camera_matrix is None:
            # Approximate for standard webcam 640x480
            self.fx = 500
            self.fy = 500
            self.cx = 320
            self.cy = 240
        else:
            self.fx = camera_matrix[0,0]
            self.fy = camera_matrix[1,1]
            self.cx = camera_matrix[0,2]
            self.cy = camera_matrix[1,2]
            
        self.logger = logging.getLogger("GraspPlanner")

    def plan_grasp_from_mask(self, mask, depth_estimate=0.5):
        """
        Calculates a grasp pose (x, y, z, roll, pitch, yaw) from a binary mask.
        Assumes a fixed depth if no depth map is provided.
        
        Args:
            mask: boolean or uint8 numpy array (H, W)
            depth_estimate: float, distance in meters from camera to object plane.
            
        Returns:
            list: [x, y, z, roll, pitch, yaw] in Camera Link Frame
        """
        ys, xs = np.where(mask)
        if len(xs) == 0:
            self.logger.warning("Empty mask provided to grasp planner")
            return None
            
        # Centroid
        u = np.mean(xs)
        v = np.mean(ys)
        
        # Pixel to Camera Frame
        # x = (u - cx) * z / fx
        # y = (v - cy) * z / fy
        
        z = depth_estimate
        x = (u - self.cx) * z / self.fx
        y = (v - self.cy) * z / self.fy
        
        # Simple top-down grasp orientation
        # Roll=0, Pitch=3.14 (pointing down), Yaw=0
        grasp_pose = [x, y, z, 0, 3.14, 0]
        
        self.logger.info(f"Planned grasp at {grasp_pose}")
        return grasp_pose
