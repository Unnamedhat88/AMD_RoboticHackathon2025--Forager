import sqlite3
import os
import datetime
import logging

class InventoryManager:
    def __init__(self, db_path="inventory.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("Inventory")
        
        # Initialize DB
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_table()
        self.logger.info(f"Connected to SQLite inventory at {self.db_path}")

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            item_name TEXT,
            category TEXT,
            status TEXT
        )
        """
        try:
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Failed to create table: {e}")

    def log_item(self, item_name, category="grocery", status="stored"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO items (timestamp, item_name, category, status) VALUES (?, ?, ?, ?)"
        try:
            self.conn.execute(query, (timestamp, item_name, category, status))
            self.conn.commit()
            self.logger.info(f"Logged item: {item_name} ({category})")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to log item: {e}")

    def get_inventory(self):
        query = "SELECT * FROM items"
        try:
            cursor = self.conn.execute(query)
            # return as list of dicts
            columns = [col[0] for col in cursor.description]
            items = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return items
        except sqlite3.Error as e:
            self.logger.error(f"Failed to fetch inventory: {e}")
            return []

    def close(self):
        self.conn.close()
