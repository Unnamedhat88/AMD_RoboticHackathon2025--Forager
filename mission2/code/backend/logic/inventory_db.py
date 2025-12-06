import json
import os
from datetime import datetime

# Define the path relative to this file
# logic/inventory_db.py -> ../data/inventory_db.json
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory_db.json')

def _load_db():
    """Load the database from the JSON file."""
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def _save_db(data):
    """Save the database to the JSON file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def add_item(item_name, category, qty=1):
    """Add a new item or update quantity if it exists."""
    db = _load_db()
    
    # Check if item already exists (simple case-insensitive match)
    for item in db:
        if item['item_name'].lower() == item_name.lower():
            item['qty'] += qty
            item['timestamp'] = datetime.now().strftime("%I:%M %p") # Update timestamp
            _save_db(db)
            return item

    # Create new item
    new_item = {
        "id": len(db) + 1, # Simple auto-increment ID
        "item_name": item_name,
        "category": category,
        "qty": qty,
        "timestamp": datetime.now().strftime("%I:%M %p")
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
        if item['item_name'].lower() == item_name.lower():
            item['qty'] = qty
            _save_db(db)
            return item
    return None

def delete_item(item_name):
    """Delete an item by name."""
    db = _load_db()
    initial_len = len(db)
    db = [item for item in db if item['item_name'].lower() != item_name.lower()]
    
    if len(db) < initial_len:
        _save_db(db)
        return True
    return False

def clear_db():
    """Clear all items from the database."""
    _save_db([])
