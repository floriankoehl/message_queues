# Message Queue — YOLO Object Detection

Asynchronous message queue service for distributing YOLO object detection jobs between a client and one or more workers.

## Components

- `mq_server.py` — REST API server managing the queues
- `mq_client.py` — submits images as jobs and collects results
- `yolo_worker.py` — pulls jobs, runs YOLO detection, pushes results
- `message_queue.py` — core queue implementation (FIFO, thread-safe, persistent)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Start each component in a separate terminal, in this order:

```bash
python mq_server.py
python yolo_worker.py
python mq_client.py
```

Run tests (requires server and worker to be running):

```bash
python test_mq.py
```

## Configuration

`config.json`:

```json
{
  "max_size": 50,
  "persistence_interval": 5
}
```

- `max_size` — maximum messages per queue
- `persistence_interval` — seconds between saves to `queues.json`

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/queues/{name}` | Create queue |
| DELETE | `/queues/{name}` | Delete queue |
| GET | `/queues` | List queues |
| POST | `/queues/{name}/messages` | Push message |
| GET | `/queues/{name}/messages` | Pop message |
