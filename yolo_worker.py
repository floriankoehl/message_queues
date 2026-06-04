from ultralytics import YOLO
import os
from message_queue import MessageQueueManager
import requests
import json
import time


# Globals
PORT = 8000
URL = f"http://localhost:{PORT}"
model = YOLO("yolov8n.pt")


# Initailize Queue
def create_transaction_queue():
    response = requests.post(f"{URL}/queues/transactions").json()
    print(response)

def create_result_queue():
    response = requests.post(f"{URL}/queues/results").json()
    print(response)

def initalize_queue():
    create_transaction_queue()
    create_result_queue()



# Execute the job
def format_detection(label, confidence, bbox):
    return {
        "label": label, 
        "condifence": confidence,
        "bbox": bbox
    }

def list_detections(results):
    detections = []
    for result in results:
        for box in result.boxes:
            label = result.names[int(box.cls)]      
            confidence = float(box.conf)             
            bbox = box.xyxy[0].tolist()            
            detected_box = format_detection(label, confidence, bbox)
            detections.append(detected_box)
        return detections

def safe_images(results, image_path):
    for result in results:
        result.save(filename=f"outputs/{os.path.basename(image_path)}")

def run_detection(image_path: str) -> list:
    if not os.path.exists(image_path):
        print(f"{image_path} does not exist - no boxes")
        return []
    try: 
        results = model(image_path)
        safe_images(results, image_path)
        return list_detections(results)

    except Exception as e: 
        print(f"YOLO error: {e}")
        return []
    
def build_result(job_id, detections):
    result = {
        "job_id": job_id,
        "detections": detections
    }
    return result



# Pop and Push
def pull_transactions():
    response = requests.get(f"{URL}/queues/transactions/messages")
            
    if response.status_code == 200: 
        data = response.json()
        return data
    else: 
        return
    
def push_results(message):
    response = requests.push(f"{URL}/queues/results/messages", json=message)

    if response.status_code == 200: 
        data = response.json()
        return data
    else: 
        print("Something went wrong when pushing results!", response)
        return 

def execute_job():
    job_id = message["job_id"]
    image_path = message["image"]

    message = pull_transactions()
    if message: 
        detections = run_detection(image_path)
        result = build_result(job_id, detections)
        push_results(result)
        print(f"Executed task on {image_path}")
        time.sleep(1)
    else: 
        time.sleep(1)



if __name__ == "__main__":
    initalize_queue()

    while True: 
        try: 
            

        except Exception as e: 
            print(str(e))
            break











