import threading
import time
import logging

class TrackerState:
    def __init__(self):
        self.lock = threading.Lock()
        # Storage: { track_id: { 'label': str, 'score': float, 'box': [], 'last_seen': ts, 'count': int } }
        self.tracked_objects = {}
        self.logger = logging.getLogger("TrackerState")

    def update(self, track_id, label, score, box, max_history=30):
        """
        Update or add a tracked object.
        """
        with self.lock:
            now = time.time()
            if track_id in self.tracked_objects:
                obj = self.tracked_objects[track_id]
                obj['last_seen'] = now
                obj['count'] += 1
                obj['score'] = score # Update confidence
                obj['box'] = box     # Update position
                # We could do moving average on box if needed, for now just replace
            else:
                self.tracked_objects[track_id] = {
                    'label': label,
                    'score': score,
                    'box': box,
                    'last_seen': now,
                    'count': 1,
                    'logged': False # Flag to check if already added to inventory
                }
    
    def prune(self, max_age_seconds=3.0):
        """
        Remove objects not seen for max_age_seconds.
        """
        with self.lock:
            now = time.time()
            to_remove = []
            for tid, obj in self.tracked_objects.items():
                if now - obj['last_seen'] > max_age_seconds:
                    to_remove.append(tid)
            
            for tid in to_remove:
                del self.tracked_objects[tid]
                # self.logger.debug(f"Pruned object {tid}")

    def get_stable_objects(self, min_seen_count=5):
        """
        Return list of objects that have been seen consistently.
        """
        with self.lock:
            stable = []
            for tid, obj in self.tracked_objects.items():
                if obj['count'] >= min_seen_count:
                    stable.append({
                        'id': int(tid),
                        'name': str(obj['label']),
                        'confidence': float(obj['score']),
                        'box': [float(c) for c in obj['box']], # Cast box coords too
                        'logged': bool(obj.get('logged', False))
                    })
            return stable

    def mark_logged(self, track_id):
        """
        Mark an object as logged to inventory.
        """
        with self.lock:
            if track_id in self.tracked_objects:
                self.tracked_objects[track_id]['logged'] = True
                return {
                    'label': self.tracked_objects[track_id]['label'],
                    'box': self.tracked_objects[track_id]['box'],
                    'score': self.tracked_objects[track_id]['score']
                }
            return None
