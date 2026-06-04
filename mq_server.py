import threading
from collections import deque





class BoundedQueue():
    def __init__(self, maxsize):
        self.queue = deque()
        self.maxsize = maxsize
        self.lock = threading.Lock()
    
    def push(self, item):
        with self.lock:
            if len(self.queue) >= self.maxsize:
                raise Exception("Queue is full!")
            else: 
                self.queue.append(item)

    def pop(self):
        with self.lock: 
            if len(self.queue) == 0: 
                raise Exception("Cant pop from empty queue!")
            else: 
                return self.queue.popleft()

    def size(self):
        with self.lock: 
            return len(self.queue)

    def to_dict(self):
        with self.lock: 
            return {
                "items": [item for item in self.queue],
                "size": len(self.queue),
                "maxsize": self.maxsize,
                "is_full": len(self.queue) >= self.maxsize
            }
    
    @classmethod
    def from_dict(cls, data):
        q = cls(data["maxsize"])
        for item in data["items"]:
            q.push(item)
        return q













