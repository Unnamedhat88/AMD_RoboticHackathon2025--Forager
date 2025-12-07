

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import cv2
import time

from perception.pose_estimator import PoseEstimator

def create_app(tracker_state, inventory, arm=None, camera_stream=None):
    app = FastAPI(title="Grocery Robot API")
    app.state.camera_stream = camera_stream
    
    # Initialize Pose Estimator
    pose_estimator = PoseEstimator()
    
    # Enable CORS for Next.js frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # For dev only
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger = logging.getLogger("API")

    @app.get("/")
    def read_root():
        return {"status": "Grocery Robot API Online"}

    @app.get("/status")
    def get_status():
        # Minimal status
        return {
            "state": "CONTINUOUS_PERCEPTION",
            "running": True
        }

    # Removed /start, /stop, /scan as they were for the manual planner
    
    @app.get("/objects")
    def get_objects():
        """Return stable tracked objects."""
        return tracker_state.get_stable_objects() # logic/TaskPlanner not needed

    @app.post("/log/{track_id}")
    def log_item(track_id: int):
        """
        Log an item to inventory by track ID.
        Returns the logged item including calculated grasp pose.
        """
        # mark_logged now returns a dict with {label, box, score} or None
        obj_data = tracker_state.mark_logged(track_id)
        
        if obj_data:
            item_name = obj_data['label']
            box = obj_data['box']
            
            # Estimate Pose
            pose = pose_estimator.estimate_pose(box)
            
            # Add to Inventory with Pose
            # Note: inventory.add_item calls inventory_db.add_item which now accepts pose
            # We need to update inventory.py wrapper first? NO, inventory.py just calls db.add_item
            # Let's check inventory.py, likely it just forwards args or we need to update it.
            # Assuming for now we can update inventory.add_item signature or pass kwargs.
            # Ideally inventory.py/InventoryManager.add_item needs update too.
            
            # Let's update InventoryManager.add_item in next step if generic, 
            # or just call db directly methods if exposed. 
            # Checking logic/inventory.py... likely simple wrapper.
            
            # For now let's assume InventoryManager abstracts it.
            # Wait, I should verify inventory.py.
            
            added_item = inventory.add_item(item_name, category="grocery", qty=1, pose=pose)
            
            return JSONResponse(content={"success": True, "item": added_item})
        
        return JSONResponse(content={"success": False, "error": "Item not found or already logged"})

    @app.get("/inventory")
    def get_inventory():
        return inventory.get_all()

    @app.post("/inventory/add")
    def add_inventory_item(item: dict):
        from logic import inventory_db
        return inventory_db.add_item(item['name'], item['category'], item.get('qty', 1))

    @app.delete("/inventory/{item_id}")
    def delete_inventory_item(item_id: int):
        success = inventory.delete_item(item_id) # integer ID to name or just ignore for now as our DB uses name
        if success:
            return {"success": True, "message": f"Item with ID {item_id} deleted."}
        else:
            return JSONResponse(status_code=404, content={"success": False, "message": f"Item with ID {item_id} not found."})

    # --- Video Streaming ---
    from fastapi.responses import StreamingResponse
    import cv2
    import time

    def generate_frames():
        while True:
            # We need access to camera_stream here. 
            # Ideally tracker_state or a global should provide it, or we pass it to create_app.
            # For now, let's assume we can pass camera_stream to create_app.
            if hasattr(app.state, 'camera_stream'):
                frame = app.state.camera_stream.read()
                if frame is None:
                    continue
                
                # Encode frame to JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                # Fallback or error
                time.sleep(0.1)
    
    @app.get("/video_feed")
    def video_feed():
        return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

    @app.get("/camera/latest")
    def get_latest_frame():
        """Return the current frame as a single JPEG image."""
        if hasattr(app.state, 'camera_stream'):
            frame = app.state.camera_stream.read()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    from fastapi.responses import Response
                    return Response(content=buffer.tobytes(), media_type="image/jpeg")
        
        # Return a placeholder or 404 if no frame
        return JSONResponse(status_code=404, content={"error": "Camera not ready"})

    return app

    @app.delete("/inventory/delete")
    def delete_inventory_item_by_name(item_name: str):
        from logic import inventory_db
        success = inventory_db.delete_item(item_name)
        return {"success": success}

    @app.post("/inventory/clear")
    def clear_inventory():
        from logic import inventory_db
        inventory_db.clear_db()
        return {"message": "Inventory cleared"}

    return app
