import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArmController")

class ArmController:
    def __init__(self, mock=True):
        self.mock = mock
        self.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # 6 DoF
        self.gripper_state = "open" # open or closed
        logger.info(f"ArmController initialized (Mock={mock})")

    def move_to_pose(self, pose):
        """Moves the arm to a specified pose (x, y, z, roll, pitch, yaw)."""
        logger.info(f"Moving to pose: {pose}")
        if self.mock:
            time.sleep(0.5) # Simulate movement delay
            self.position = pose
            logger.info("Movement complete.")
            return True
        else:
            # TODO: Implement real hardware control via ROS2
            pass
    
    def open_gripper(self):
        logger.info("Opening gripper...")
        if self.mock:
            self.gripper_state = "open"
            time.sleep(0.2)
            return True

    def close_gripper(self):
        logger.info("Closing gripper...")
        if self.mock:
            self.gripper_state = "closed"
            time.sleep(0.2)
            return True

    def get_status(self):
        return {
            "position": self.position,
            "gripper": self.gripper_state
        }
