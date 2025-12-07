import logging
import subprocess
import threading
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArmController")

class ArmController:
    def __init__(self, mock=False):
        self.mock = mock or os.getenv("USE_ARM", "true").lower() == "false"
        self.lock = threading.Lock()
        self.is_moving = False
        logger.info(f"ArmController initialized (Mock={self.mock})")

    def execute_policy(self, task_name="pickup the cube"):
        """
        Executes a lerobot policy via subprocess.
        This is a blocking call if run directly, so it should be threaded.
        """
        if self.mock:
            logger.info(f"[MOCK] Executing policy for task: {task_name}")
            time.sleep(3) # Simulate duration
            logger.info("[MOCK] Policy execution complete.")
            return True

        with self.lock:
            if self.is_moving:
                logger.warning("Arm is already moving. Ignoring request.")
                return False
            self.is_moving = True

        try:
            logger.info(f"Starting policy execution: {task_name}")
            
            # Command from user request
            cmd = [
                "/home/amddemo/miniconda3/envs/lerobot/bin/lerobot-record",
                "--robot.type=so101_follower",
                "--robot.port=/dev/ttyACM1",
                "--robot.id=my_awesome_follower_arm",
                '--robot.cameras={"top": {"type": "opencv", "index_or_path": "/dev/video5", "width": 640, "height": 480, "fps": 30}, "side": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30}}',
                f"--dataset.single_task={task_name}",
                "--dataset.repo_id=Unnnamedhat88/eval_AMD_FORAGER",
                "--policy.path=/home/amddemo/.cache/huggingface/hub/models--Unnnamedhat88--AMD_FORAGER/snapshots/b29d31a44168d861b23c657494c6c3285a10b62b/checkpoints/010000/pretrained_model"
            ]

            # Use subprocess to run the command
            # capture_output=True to log stdout/stderr if needed
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Policy executed successfully.")
                logger.debug(result.stdout)
                return True
            else:
                logger.error(f"Policy execution failed with code {result.returncode}")
                logger.error(result.stderr)
                return False

        except Exception as e:
            logger.error(f"Error executing policy: {e}")
            return False
        finally:
            with self.lock:
                self.is_moving = False
