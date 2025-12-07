import json
import os
import fcntl
from datetime import datetime

# Define the path relative to this file
# logic/inventory_db.py -> ../data/inventory_db.json
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory_db.json')

def _load_db():
    """Load the database from the JSON file with shared lock."""
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, 'r') as f:
            try:
                fcntl.flock(f, fcntl.LOCK_SH)
                return json.load(f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    except (json.JSONDecodeError, IOError):
        return []

def _save_db(data):
    """Save the database to the JSON file with exclusive lock."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX)
            json.dump(data, f, indent=4)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

def add_item(item_name, category, qty=1, pose=None):
    """Add a new item or update quantity if it exists."""
    # ...
    
    db = _load_db()
    
    # Check if item already exists (simple case-insensitive match)
    for item in db:
        if item.get('name', '').lower() == item_name.lower():
            item['qty'] += qty
            item['timestamp'] = datetime.now().strftime("%d/%m/%y %I:%M %p") # Update timestamp
            if pose:
                item['pose'] = pose # Update pose if provided
            _save_db(db)
            return item

    # Create new item
    new_item = {
        "id": len(db) + 1, # Simple auto-increment ID
        "name": item_name,
        "category": category,
        "qty": qty,
        "timestamp": datetime.now().strftime("%d/%m/%y %I:%M %p"),
        "pose": pose # Store pose
    }
    db.append(new_item)
    _save_db(db)
    return new_item

def get_all_items():
    """Retrieve all items from the database."""
    return _load_db()

def update_item_qty(item_name, qty):
    """Update the quantity of a specific item."""
    db = _load_db()
    for item in db:
        if item.get('name', '').lower() == item_name.lower():
            item['qty'] = qty
            _save_db(db)
            return item
    return None

def delete_item(item_name):
    """Delete an item by name."""
    db = _load_db()
    initial_len = len(db)
    db = [item for item in db if item.get('name', '').lower() != item_name.lower()]
    
    if len(db) < initial_len:
        _save_db(db)
        return True
    return False

def delete_item_by_id(item_id):
    """Delete an item by ID."""
    db = _load_db()
    initial_len = len(db)
    db = [item for item in db if item.get('id') != item_id]
    
    if len(db) < initial_len:
        _save_db(db)
        return True
    return False

def clear_db():
    """Clear all items from the database."""
    _save_db([])
