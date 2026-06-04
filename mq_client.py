

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
    run_all()





