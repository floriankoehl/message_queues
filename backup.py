




def format_detection(label, confidence, bbox):
    return {
        "label": label, 
        "condifence": confidence,
        "bbox": bbox
    }





from utils import format_detection
from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

def run_detection(image_path: str) -> list:
    if not os.path.exists(image_path):
        return []

    try: 
        results = model(image_path)
        detections = []
        for result in results:
            for box in result.boxes:
                label = result.names[int(box.cls)]      
                confidence = float(box.conf)             
                bbox = box.xyxy[0].tolist()            
                detected_box = format_detection(label, confidence, bbox)
                detections.append(detected_box)
        return detections
    
    except Exception as e: 
        print(f"YOLO error: {e}")
        return []


boxes = run_detection("data/image.jpg")
for box in boxes: 
    print(box)


















import time



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




class RateLimiter():
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
        self.lock = threading.Lock()

    def allow(self, key):
        now = time.time()

        with self.lock:
            request_times = self.requests.get(key, deque())

            while request_times and now - request_times[0] >= self.window_seconds:
                request_times.popleft()

            if len(request_times) >= self.max_requests:
                self.requests[key] = request_times
                return False

            request_times.append(now)
            self.requests[key] = request_times
            return True




from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json



app = FastAPI()

class Item(BaseModel):
    job: str

with open("config.json", "r") as file: 
    config = json.load(file)
max_size = config["max_size"]
queue = BoundedQueue(max_size)
rate_limiter = RateLimiter(
    max_requests=config.get("rate_limit_max_requests", 10),
    window_seconds=config.get("rate_limit_window_seconds", 60)
)


def check_rate_limit(request: Request):
    client = request.client.host if request.client else "unknown"
    if not rate_limiter.allow(client):
        return JSONResponse(
            status_code=429,
            content={"error": "Too many requests"}
        )

    return None



@app.post("/push")
def push(item: Item, request: Request):
    rate_limit_response = check_rate_limit(request)
    if rate_limit_response:
        return rate_limit_response

    try: 
        queue.push(item.job)
        return {"queue": [item for item in queue.queue]}
    except Exception as e: 
        return JSONResponse(
            status_code=409,
            content={"error": str(e)}
        )



@app.post("/pop")
def pop(request: Request):
    rate_limit_response = check_rate_limit(request)
    if rate_limit_response:
        return rate_limit_response

    try:
        item = queue.pop()
        return {"item": item}
    except Exception as e: 
        return JSONResponse(
            status_code=404, 
            content={"error": str(e)}
        )
        


@app.get("/get_items")
def get_items(request: Request):
    rate_limit_response = check_rate_limit(request)
    if rate_limit_response:
        return rate_limit_response

    return [item for item in queue.queue]


















import requests
import json

PORT = 8000
URL = f"http://localhost:{PORT}"
queue_name = "test_queue"

def check_health():
    response = requests.get(f"{URL}/health")
    print(response.json()["message"])


def create_test_queue():
    response = requests.post(f"{URL}/queues/{queue_name}").json()
    print(response)


def remove_test_queue():
    response = requests.delete(f"{URL}/queues/{queue_name}").json()
    print(response)

def push_message():
    requests.post(f"{URL}/queues/{queue_name}")

    example_message = {
        "job_id": 123, 
        "image": "data/image.jpg"
    }
    response = requests.post(f"{URL}/queues/{queue_name}/messages", json=example_message)
    print(response.json())    
    list = requests.get(f"{URL}/get_queue_content/{queue_name}").json()
    print(list)

    response = requests.get(f"{URL}/queues/{queue_name}/messages").json()
    print("POPPED HERR", response)

    list = requests.get(f"{URL}/get_queue_content/{queue_name}").json()
    print(list)

def run_all():
    check_health()
    create_test_queue()
    remove_test_queue()
    push_message()


























if __name__ == "__main__":
    # run_all()










