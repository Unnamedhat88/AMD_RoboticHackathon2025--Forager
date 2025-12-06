
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

def create_app(tracker_state, inventory, arm=None):
    app = FastAPI(title="Grocery Robot API")
    
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
    def log_tracked_item(track_id: int):
        """Log a specific tracked item to inventory."""
        label = tracker_state.mark_logged(track_id)
        if label:
            from logic import inventory_db
            db_item = inventory_db.add_item(label, "grocery", 1)
            return {"success": True, "item": db_item}
        else:
            return {"success": False, "error": "Item not found or already logged"}

    @app.get("/inventory")
    def get_inventory():
        return planner.inventory.get_all()

    @app.post("/inventory/add")
    def add_inventory_item(item: dict):
        from logic import inventory_db
        return inventory_db.add_item(item['name'], item['category'], item.get('qty', 1))

    @app.delete("/inventory/{item_id}")
    def delete_inventory_item(item_id: int):
        success = planner.inventory.delete_item(item_id)
        if success:
            return {"success": True, "message": f"Item {item_id} deleted"}
        return JSONResponse(status_code=404, content={"success": False, "message": "Item not found"})

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
