from ultralytics import YOLO
import os
from message_queue import MessageQueueManager
import requests
import json
import time

model = YOLO("yolov8n.pt")

def format_detection(label, confidence, bbox):
    return {
        "label": label, 
        "condifence": confidence,
        "bbox": bbox
    }

def run_detection(image_path: str) -> list:
    if not os.path.exists(image_path):
        return []

    try: 
        results = model(image_path)
        detections = []
        for result in results:

            # Safe results
            result.save(filename=f"outputs/{os.path.basename(image_path)}")

            # Prepare response message
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


# boxes = run_detection("data/image.jpg")
# for box in boxes: 
#     print(box)


PORT = 8000
URL = f"http://localhost:{PORT}"




# Initailize Queue
def create_transaction_queue():
    response = requests.post(f"{URL}/queues/transactions").json()
    print(response)

def create_result_queue():
    response = requests.post(f"{URL}/queues/results").json()
    print(response)

def create_infrastructure():
    create_transaction_queue()
    create_result_queue()






# Pull from Queue
def pull_transactions():
    response = requests.get(f"{URL}/queues/transactions/messages")
            
    if response.status_code == 200: 
        data = response.json()
        return data
    else: 
        return



def execute_job(message):
    print("Inside execute job")
    image_path = message["image"]
    run_detection(image_path)
    print(f"Executed task on {image_path}")
    time.sleep(1)
    pass



if __name__ == "__main__":
    create_infrastructure()

    while True: 
        try: 
            data = pull_transactions()
            if data: 
                execute_job(data)
            else: 
                time.sleep(1)

        except Exception as e: 
            print(str(e))
            break











