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

    @app.get("/inventory")
    def get_inventory():
        return inventory.get_inventory()

    return app
