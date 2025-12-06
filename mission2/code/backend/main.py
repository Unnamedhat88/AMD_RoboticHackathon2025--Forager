import time
import logging
from perception.camera import CameraInterface
from manipulation.arm_controller import ArmController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

def main():
    logger.info("Starting Grocery Sorting Robot System...")
    
    # Initialize components
    # Initialize components
    # Phase 1.A: Force mock camera
    camera = CameraInterface(mock=True)
    arm = ArmController(mock=True)
    
    # Initialize Perception & Manipulation & Logic
    try:
        from perception.detector import GroceryDetector
        from perception.segmenter import GrocerySegmenter
        from manipulation.grasp_planner import GraspPlanner
        from logic.task_planner import TaskPlanner
        from logic.inventory import InventoryManager
        from api import create_app
        import threading
        import uvicorn
        
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
        # Start Planner Thread
        planner_thread = threading.Thread(target=planner.run_loop, daemon=True)
        planner_thread.start()
        logger.info("Planner thread started.")
        
        # Start API Server
        logger.info("Starting API Server on port 8000...")
        app = create_app(planner, inventory)
        uvicorn.run(app, host="0.0.0.0", port=8000)

    except KeyboardInterrupt:
        logger.info("Stopping system...")
    finally:
        camera.release()
        logger.info("System shutdown.")

if __name__ == "__main__":
    main()
