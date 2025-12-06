import time
import logging
from perception.camera import CameraInterface
from manipulation.arm_controller import ArmController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

def main():
    logger.info("Starting Grocery Sorting Robot System...")
    
    # Initialize components
    camera = CameraInterface(mock=False) # Try real camera, fallback to mock if fails? Handled in class.
    # Actually, CameraInterface default was mock=True. Let's stick to mock for now unless we are sure.
    # The plan said "Implement camera interface (Real/Mock)". Let's leave it as is but initialize detector.
    camera = CameraInterface(mock=True)
    arm = ArmController(mock=True)
    
    # Initialize Perception & Manipulation & Logic
    try:
        from perception.detector import GroceryDetector
        from perception.segmenter import GrocerySegmenter
        from manipulation.grasp_planner import GraspPlanner
        from logic.task_planner import TaskPlanner
        from logic.inventory import InventoryManager
        
        detector = GroceryDetector()
        segmenter = GrocerySegmenter()
        grasp_planner = GraspPlanner()
        inventory = InventoryManager()
        
        # Initialize Planner
        planner = TaskPlanner(camera, arm, detector, segmenter, grasp_planner, inventory)
        
    except Exception as e:
        logger.error(f"Failed to initialize modules: {e}")
        return

    try:
        # Run state machine
        logger.info("Starting Task Planner Loop...")
        planner.run(cycles=10)

    except KeyboardInterrupt:
        logger.info("Stopping system...")
    finally:
        camera.release()
        logger.info("System shutdown.")

if __name__ == "__main__":
    main()
