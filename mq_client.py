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
    # create_infrastructure()
    
    message = {
        "job_id": "123",
        "image": "data/image.jpg"
    }
    push_to_transactions(message)
    push_to_transactions(message)
    push_to_transactions(message)
    push_to_transactions(message)
    

















