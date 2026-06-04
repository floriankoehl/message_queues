import threading
from collections import deque
import json



with open("config.json", "r") as f: 
    config = json.load(f)




class MessageQueue():
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








class MessageQueueManager():
    def __init__(self):
        self.queues = {}
        self.lock = threading.Lock()

    def create_queue(self, name):
        with self.lock:
            if name in self.queues: 
                raise Exception("Queue already exists")
            else: 
                self.queues[name] = MessageQueue(config["max_size"])

    def delete_queue(self, name):
        with self.lock:
            if name not in self.queues: 
                raise Exception("Queue name not found - can not delete queue which is not there!")
            else: 
                del self.queues[name]

    def list_queues(self):
        return self.queues
    
    def get_queue_content(self, name):
        if name not in self.queues:
            raise Exception("Queue does not exist - cant get content")
        else: 
            return list(self.queues[name].queue)
    
    def push(self, name, message):
        with self.lock:
            if name not in self.queues: 
                raise Exception("Queue not found - can not push elements to non existing queue!")
            else: 
                self.queues[name].push(message)

    def pop(self, name):
        with self.lock:
            if name not in self.queues: 
                raise Exception("Queue not found - can not pop elements from non existing queue!")
            else: 
                message = self.queues[name].pop()
                return message








