import logging
from logic import inventory_db

class InventoryManager:
    def __init__(self):
        self.logger = logging.getLogger("Inventory")
        self.logger.info("Initialized InventoryManager with JSON DB")

    def log_item(self, item_name, category="grocery", status="stored"):
        # Map log_item to add_item
        # Note: 'status' is not currently used in the simple JSON schema, 
        # but we could add it if needed. For now, we just track name, category, qty.
        try:
            result = inventory_db.add_item(item_name, category)
            self.logger.info(f"Logged item: {item_name} ({category})")
            return result
        except Exception as e:
            self.logger.error(f"Failed to log item: {e}")
            return None

    def get_inventory(self):
        try:
            return inventory_db.get_all_items()
        except Exception as e:
            self.logger.error(f"Failed to fetch inventory: {e}")
            return []

    def close(self):
        pass # No connection to close

