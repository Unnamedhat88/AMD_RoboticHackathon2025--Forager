import logging
from logic import inventory_db

class InventoryManager:
    def __init__(self):
        self.logger = logging.getLogger("Inventory")
        self.logger.info("Initialized InventoryManager with JSON DB")

    def log_item(self, item_name, category="grocery", status="stored", qty=1, pose=None):
        # Map log_item to add_item
        # Note: 'status' is not currently used in the simple JSON schema, 
        # but we could add it if needed. For now, we just track name, category, qty.
        try:
            result = inventory_db.add_item(item_name, category, qty, pose)
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

    def get_all(self):
        """Alias for get_inventory to match API spec."""
        return self.get_inventory()

    def delete_item(self, item_id):
        try:
            return inventory_db.delete_item_by_id(item_id)
        except Exception as e:
            self.logger.error(f"Failed to delete item {item_id}: {e}")
            return False

    def close(self):
        pass # No connection to close

    def add_item(self, item_name, category="grocery", qty=1, pose=None):
        return self.log_item(item_name, category=category, qty=qty, pose=pose)

