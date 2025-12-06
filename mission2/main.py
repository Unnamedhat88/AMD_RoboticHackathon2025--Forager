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
    
    # Initialize Perception & Manipulation
    try:
        from perception.detector import GroceryDetector
        from perception.segmenter import GrocerySegmenter
        from manipulation.grasp_planner import GraspPlanner
        
        detector = GroceryDetector()
        segmenter = GrocerySegmenter()
        grasp_planner = GraspPlanner()
    except Exception as e:
        logger.error(f"Failed to initialize modules: {e}")
        return

    try:
        # Simple test loop
        for i in range(3):
            logger.info(f"--- Cycle {i+1} ---")
            
            # Perception step
            frame = camera.get_frame()
            logger.info(f"Captured frame with shape {frame.shape}")
            
            # Detect objects
            prompts = ["grocery item", "bottle", "fruit"]
            detections = detector.detect_objects(frame, prompts)
            logger.info(f"Detected {len(detections)} objects: {[d['label'] for d in detections]}")
            
            # Segment & Plan Grasp
            if detections:
                boxes = [d['box'] for d in detections]
                masks = segmenter.segment_objects(frame, boxes)
                logger.info(f"Generated {len(masks)} masks")
                
                # Pick the first object
                target_pose = grasp_planner.plan_grasp_from_mask(masks[0])
                if target_pose:
                     logger.info(f"Planned grasp pose: {target_pose}")
                     
                     # Manipulation step
                     arm.move_to_pose(target_pose)
                     arm.close_gripper()
                     time.sleep(0.5)
                     # Lift up (Z + 0.2)
                     lift_pose = list(target_pose)
                     lift_pose[2] += 0.2
                     arm.move_to_pose(lift_pose) 
                     arm.open_gripper()
            else:
                logger.info("No objects detected, skipping manipulation.")
            
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Stopping system...")
    finally:
        camera.release()
        logger.info("System shutdown.")

if __name__ == "__main__":
    main()
