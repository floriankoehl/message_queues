import requests
import json
import os

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

def push_imamges_from_dir(dir: str) -> list:
    files = os.listdir(f"{dir}/")
    print(files)

    for index, file in enumerate(files): 
        message = build_message(index, f"{dir}/{file}")
        push_to_transactions(message)
    

    

def pop_from_results():
    response = requests.get(f"{URL}/queues/results/messages")

    if response.status_code == 200: 
        data = response.json()
        print("POPPED SUCESFULLY: ", data)
        return data
    else: 
        print("Something went wrong popping")
        






if __name__ == "__main__":
    results = []

    while True: 
        try: 
            result = pop_from_results()
            results.append(result)
        except Exception as e: 
            print(str(e))
            break





















