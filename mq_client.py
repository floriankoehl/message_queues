import requests
import json
import os
import time

PORT = 8000
URL = f"http://localhost:{PORT}"



def push_to_transactions(message):
    response = requests.post(f"{URL}/queues/transactions/messages",
                             json=message).json()

    print(response)

def build_message(job_id, image_path):
    return {
            "job_id": job_id,
            "image": image_path
            }

def push_imamges_from_dir(dir: str) -> int:
    files = os.listdir(f"{dir}/")
    print(files)

    for index, file in enumerate(files):
        message = build_message(index, f"{dir}/{file}")
        push_to_transactions(message)
    return len(files)
    
def pop_from_results():
    response = requests.get(f"{URL}/queues/results/messages")

    if response.status_code == 200: 
        data = response.json()
        print("POPPED SUCESFULLY: ", data)
        return data
    else: 
        time.sleep(1)
        






if __name__ == "__main__":
    count = push_imamges_from_dir("data")

    results = []
    while len(results) < count:
        result = pop_from_results()
        if result:
            results.append(result)





















