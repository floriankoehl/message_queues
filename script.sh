#!/bin/bash

cd "$(dirname "$0")"

source .venv/bin/activate

python mq_server.py &
sleep 2

python yolo_worker.py &
sleep 1

python mq_client.py