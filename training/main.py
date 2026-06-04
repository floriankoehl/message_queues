
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






