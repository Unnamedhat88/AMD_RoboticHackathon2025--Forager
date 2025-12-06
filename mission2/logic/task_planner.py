import logging
import time
from enum import Enum

class State(Enum):
    IDLE = 0
    PERCEIVE = 1
    PICK = 2
    PLACE = 3
    LOG = 4

class TaskPlanner:
    def __init__(self, camera, arm, detector, segmenter, grasp_planner, inventory):
        self.camera = camera
        self.arm = arm
        self.detector = detector
        self.segmenter = segmenter
        self.grasp_planner = grasp_planner
        self.inventory = inventory
        
        self.state = State.IDLE
        self.logger = logging.getLogger("TaskPlanner")
        self.current_target_pose = None
        self.current_item_label = None

    def update_state(self):
        """
        Main state machine loop step.
        """
        if self.state == State.IDLE:
            self.logger.info("State: IDLE -> PERCEIVE")
            self.state = State.PERCEIVE
            
        elif self.state == State.PERCEIVE:
            self.logger.info("State: PERCEIVE")
            frame = self.camera.get_frame()
            
            # Detect
            prompts = ["grocery item", "bottle", "fruit", "can", "box"]
            detections = self.detector.detect_objects(frame, prompts)
            
            if not detections:
                self.logger.info("No objects found. Retry IDLE.")
                self.state = State.IDLE
                time.sleep(1)
                return

            self.logger.info(f"Found {len(detections)} objects.")
            
            # Segment first object
            # For simplicity, pick the one with highest score
            best_det = max(detections, key=lambda x: x['score'])
            self.current_item_label = best_det['label']
            
            masks = self.segmenter.segment_objects(frame, [best_det['box']])
            target_pose = self.grasp_planner.plan_grasp_from_mask(masks[0])
            
            if target_pose:
                self.current_target_pose = target_pose
                self.state = State.PICK
            else:
                self.logger.warning("Could not plan grasp. Retry.")
                self.state = State.IDLE

        elif self.state == State.PICK:
            self.logger.info(f"State: PICK ({self.current_item_label})")
            
            # Move to Pre-grasp (above target)
            pre_grasp = list(self.current_target_pose)
            pre_grasp[2] += 0.15
            
            self.arm.open_gripper()
            self.arm.move_to_pose(pre_grasp)
            
            # Move to Grasp
            self.arm.move_to_pose(self.current_target_pose)
            self.arm.close_gripper()
            time.sleep(0.5)
            
            # Lift
            self.arm.move_to_pose(pre_grasp)
            
            self.state = State.PLACE

        elif self.state == State.PLACE:
            self.logger.info("State: PLACE")
            # Define a fixed bin location
            bin_pose = [-0.3, 0.0, 0.4, 0, 3.14, 0] 
            
            self.arm.move_to_pose(bin_pose)
            self.arm.open_gripper()
            time.sleep(0.5)
            
            self.state = State.LOG

        elif self.state == State.LOG:
            self.logger.info("State: LOG")
            if self.current_item_label:
                self.inventory.log_item(self.current_item_label)
            
            # Reset and go back to IDLE
            self.current_target_pose = None
            self.current_item_label = None
            self.state = State.IDLE
            time.sleep(1)
            
    def run(self, cycles=5):
        for _ in range(cycles):
            try:
                self.update_state()
            except Exception as e:
                self.logger.error(f"Error in state machine: {e}")
                break
