from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

def create_app(planner, inventory):
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
        return planner.get_status()

    @app.post("/start")
    def start_robot():
        planner.start()
        return {"message": "Robot started"}

    @app.post("/stop")
    def stop_robot():
        planner.stop()
        return {"message": "Robot stopped"}

    @app.post("/scan")
    def scan_item():
        """Trigger a manual scan and log."""
        result = planner.scan_and_log()
        return {"message": "Scan complete", "result": result}

    @app.get("/inventory")
    def get_inventory():
        # Use the new DB logic directly
        from logic import inventory_db
        return inventory_db.get_all_items()

    @app.post("/inventory/add")
    def add_inventory_item(item: dict):
        from logic import inventory_db
        return inventory_db.add_item(item['item_name'], item['category'], item.get('qty', 1))

    @app.delete("/inventory/delete")
    def delete_inventory_item(item_name: str):
        from logic import inventory_db
        success = inventory_db.delete_item(item_name)
        return {"success": success}

    @app.post("/inventory/clear")
    def clear_inventory():
        from logic import inventory_db
        inventory_db.clear_db()
        return {"message": "Inventory cleared"}

    return app
