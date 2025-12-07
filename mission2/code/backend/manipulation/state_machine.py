import threading
import logging
import time

logger = logging.getLogger("StateMachine")

class ScanStateMachine:
    def __init__(self, arm_controller):
        self.arm = arm_controller
        self.is_running = False
        self.lock = threading.Lock()

    def run_scan_routine(self, task_name="pickup the cube"):
        """
        Triggers the Scan & Sort routine in a background thread.
        Returns check: (True, "Started") or (False, "Busy")
        """
        with self.lock:
            if self.is_running:
                return False, "Robot is busy"
            self.is_running = True
        
        # Start background thread
        t = threading.Thread(target=self._routine, args=(task_name,))
        t.daemon = True
        t.start()
        
        return True, "Scan routine started"

    def _routine(self, task_name):
        logger.info("Starting Scan Routine...")
        try:
            # 1. Execute Arm Policy (Pick -> Spin -> Drop)
            success = self.arm.execute_policy(task_name)
            
            if success:
                logger.info("Arm routine finished successfully.")
                # 2. Wait for perception stability?
                # The perception loop is continuous, so it will naturally pick up the item 
                # once it is stable. No explicit "wait" needed here unless we want to poll until logged.
            else:
                logger.error("Arm routine failed.")
                
        except Exception as e:
            logger.error(f"Routine exception: {e}")
        finally:
            with self.lock:
                self.is_running = False
            logger.info("Scan Routine complete/reset.")
