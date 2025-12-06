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
        self.inventory = inventory
        self.running = False
        
        self.state = State.IDLE
        self.logger = logging.getLogger("TaskPlanner")
        self.current_target_pose = None
        self.current_item_label = None

    def update_state(self):
        """
        Main state machine loop step.
        """
        if self.state == State.IDLE:
            # Only transition if running, otherwise just stay idle
            if self.running:
                self.logger.info("State: IDLE -> PERCEIVE")
                self.state = State.PERCEIVE
            else:
                time.sleep(0.1)
            
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
            
    def start(self):
        self.running = True
        self.logger.info("TaskPlanner started.")

    def scan_and_log(self):
        """
        Phase 1.A: Manual scan trigger.
        Captures frame, detects item, logs to DB.
        """
        self.logger.info("Manual Scan Triggered")
        
        # 1. Capture
        frame = self.camera.capture_frame()
        
        # 2. Detect
        # Note: detect_item is the mock method we added
        result = self.detector.detect_item(frame)
        
        # 3. Log
        # New detector returns "name" and "confidence"
        item_label = result.get('name', "Unknown")
        confidence = result.get('confidence', 0.0)
        
        self.logger.info(f"Detected: {item_label} (Score: {confidence:.2f})")
        
        # Use the inventory manager to log (it wraps the DB logic)
        if item_label != "Unknown Item":
             db_item = self.inventory.log_item(item_label, category="grocery", status="manual_scan")
        else:
             db_item = None
        
        # 4. Return formatted result
        if db_item:
            return {
                "name": db_item['name'],
                "quantity": db_item['qty'],
                "confidence": confidence
            }
        else:
            # Fallback if DB log failed or unknown item
            return {
                "name": item_label,
                "quantity": 0 if item_label == "Unknown Item" else 1, 
                "confidence": confidence,
                "error": "Not logged" if item_label == "Unknown Item" else "Failed to log to DB"
            }

    def stop(self):
        self.running = False
        self.logger.info("TaskPlanner stopped.")

    def get_status(self):
        return {
            "state": self.state.name,
            "running": self.running,
            "current_item": self.current_item_label
        }

    def run_loop(self):
        self.logger.info("TaskPlanner loop running...")
        while True:
            # We can use a separate flag for the thread loop vs the logic 'running'
            # But for simplicity, let's just loop forever and check self.running inside update_state
            # or break if we want to kill the thread.
            # Let's assume the thread runs forever but only does work if self.running is True.
            try:
                self.update_state()
            except Exception as e:
                self.logger.error(f"Error in state machine: {e}")
                time.sleep(1)
            time.sleep(0.1)
