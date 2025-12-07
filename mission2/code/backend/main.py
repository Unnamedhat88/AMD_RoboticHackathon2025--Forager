import time
import logging
import threading
import uvicorn
from api import create_app

# New imports
from perception.camera_stream import CameraStream
from perception.tracker_state import TrackerState
from perception.continuous_detector import PerceptionLoop
from logic.inventory import InventoryManager

# Keep ArmController for now, though not heavily used yet
from manipulation.arm_controller import ArmController

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

def main():
    logger.info("Starting Grocery Sorting Robot System (Phase 2.C)...")
    
    # 1. Initialize Threaded Camera
    camera = CameraStream(src=6).start()
    time.sleep(1.0) # Warmup
    
    # 2. Initialize Tracker State
    tracker_state = TrackerState()
    
    # 3. Initialize Perception Loop
    detector = PerceptionLoop(camera, tracker_state)
    detector.start()
    
    # 4. Initialize Other Components
    inventory = InventoryManager()
    arm = ArmController(mock=True) # Phase 1 artifact
    
    # Note: TaskPlanner is temporarily bypassed/deprecated in Phase 2.C 
    # as we move to a continuous decoupled architecture.
    # Logic will move to consuming tracker_state.
    
    try:
        # Start API Server
        logger.info("Starting API Server on port 8000...")
        # We pass tracker_state to the API instead of planner
        app = create_app(tracker_state, inventory, arm, camera_stream=camera)
        uvicorn.run(app, host="0.0.0.0", port=8000)

    except KeyboardInterrupt:
        logger.info("Stopping system...")
    finally:
        detector.stop()
        camera.stop()
        logger.info("System shutdown.")

if __name__ == "__main__":
    main()
