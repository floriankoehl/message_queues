import requests
import json


PORT = 8000
URL = f"http://localhost:{PORT}"



# # Initailize Queue
# def create_transaction_queue():
#     response = requests.post(f"{URL}/queues/transactions").json()
#     print(response)

# def create_result_queue():
#     response = requests.post(f"{URL}/queues/results").json()
#     print(response)

# def create_infrastructure():
#     create_transaction_queue()
#     create_result_queue()


def push_to_transactions(message):
    response = requests.post(f"{URL}/queues/transactions/messages",
                             json=message).json()

    print(response)










if __name__ == "__main__":

    for i in range(7):
        j = ""
        if i == 6: 
            j = ""
        else: 
            j = f"_{i}"

        push_to_transactions({
            "job_id": f"{i}",
            "image": f"data/image{j}.jpg"
        })





















