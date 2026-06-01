import requests
import uuid
import time

SERVER = "http://localhost:8000"


# -------------------------
# helper
# -------------------------
def print_ok(msg):
    print(f"✅ {msg}")


def print_fail(msg):
    print(f"❌ {msg}")


def create_fresh_queue():
    name = f"test_{uuid.uuid4().hex[:6]}"
    requests.post(f"{SERVER}/queues/{name}")
    return name


# -------------------------
# TEST 1: create queue
# -------------------------
def test_create_queue():
    print("\nTEST: create queue")

    name = f"test_{uuid.uuid4().hex[:6]}"
    r = requests.post(f"{SERVER}/queues/{name}")

    if r.status_code == 200:
        print_ok("Queue created")
    else:
        print_fail(r.json())


# -------------------------
# TEST 2: list queues
# -------------------------
def test_list_queues():
    print("\nTEST: list queues")

    r = requests.get(f"{SERVER}/queues")

    if r.status_code == 200 and isinstance(r.json(), list):
        print_ok("Queues listed")
    else:
        print_fail("Failed to list queues")


# -------------------------
# TEST 3: push / pop
# -------------------------
def test_push_pop():
    print("\nTEST: push / pop")

    queue = create_fresh_queue()

    msg = {"id": 1}
    requests.post(f"{SERVER}/queues/{queue}/messages", json=msg)

    r = requests.get(f"{SERVER}/queues/{queue}/messages")

    if r.status_code == 200 and r.json() == msg:
        print_ok("Push/Pop works")
    else:
        print_fail(f"Expected {msg}, got {r.json()}")


# -------------------------
# TEST 4: FIFO
# -------------------------
def test_fifo():
    print("\nTEST: FIFO")

    queue = create_fresh_queue()

    requests.post(f"{SERVER}/queues/{queue}/messages", json={"id": 1})
    requests.post(f"{SERVER}/queues/{queue}/messages", json={"id": 2})
    requests.post(f"{SERVER}/queues/{queue}/messages", json={"id": 3})

    r1 = requests.get(f"{SERVER}/queues/{queue}/messages").json()
    r2 = requests.get(f"{SERVER}/queues/{queue}/messages").json()
    r3 = requests.get(f"{SERVER}/queues/{queue}/messages").json()

    if [r1, r2, r3] == [{"id": 1}, {"id": 2}, {"id": 3}]:
        print_ok("FIFO order correct")
    else:
        print_fail(f"Wrong order: {r1}, {r2}, {r3}")


# -------------------------
# TEST 5: queue not exist
# -------------------------
def test_queue_not_exist():
    print("\nTEST: queue not exist")

    r = requests.get(f"{SERVER}/queues/not_exist/messages")

    if r.status_code != 200:
        print_ok("Handled non-existent queue")
    else:
        print_fail("Should return error")


# -------------------------
# TEST 6: queue full
# -------------------------
def test_queue_full():
    print("\nTEST: queue full")

    queue = create_fresh_queue()

    detected = False

    for i in range(200):
        r = requests.post(
            f"{SERVER}/queues/{queue}/messages",
            json={"i": i}
        )

        if r.status_code != 200:
            detected = True
            break

    if detected:
        print_ok("Queue full handled")
    else:
        print_fail("Queue overflow not detected")


# -------------------------
# TEST 7: worker flow
# -------------------------
def test_worker_flow():
    print("\nTEST: worker flow")

    job_id = str(uuid.uuid4())

    job = {
        "job_id": job_id,
        "image": "data/image.jpg"
    }

    requests.post(
        f"{SERVER}/queues/transactions/messages",
        json=job
    )

    start = time.time()
    timeout = 20

    while True:
        if time.time() - start > timeout:
            print_fail("Worker timeout")
            return

        r = requests.get(f"{SERVER}/queues/results/messages")

        if r.status_code != 200:
            time.sleep(1)
            continue

        data = r.json()

        if data.get("job_id") == job_id:
            print_ok("Worker processed job")
            return

        time.sleep(1)

def test_thread_safety():
    print("\nTEST: thread safety")

    queue = create_fresh_queue()
    total = 50

    import threading

    def producer(i):
        requests.post(
            f"{SERVER}/queues/{queue}/messages",
            json={"id": i}
        )

    threads = []

    for i in range(total):
        t = threading.Thread(target=producer, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # collect results
    results = []

    for _ in range(total):
        r = requests.get(f"{SERVER}/queues/{queue}/messages").json()
        results.append(r["id"])

    if len(set(results)) == total:
        print("✅ Thread safe")
    else:
        print("❌ Race condition detected")


def test_persistence():
    print("\nTEST: persistence")

    queue = create_fresh_queue()

    msg = {"id": 999}

    requests.post(
        f"{SERVER}/queues/{queue}/messages",
        json=msg
    )

    print("⚠️ Please restart the server NOW and press Enter...")
    input()
    time.sleep(1)

    r = requests.get(f"{SERVER}/queues/{queue}/messages")

    if r.status_code == 200 and r.json() == msg:
        print("✅ Persistence works")
    else:
        print("❌ Data lost after restart")


def test_multiple_workers():
    print("\nTEST: multiple workers")

    NUM_JOBS = 10
    job_ids = set()
    results = set()

    for _ in range(NUM_JOBS):
        job_id = str(uuid.uuid4())
        job_ids.add(job_id)

        requests.post(
            f"{SERVER}/queues/transactions/messages",
            json={
                "job_id": job_id,
                "image": "data/image.jpg"
            }
        )

    print("Jobs submitted:", job_ids)
    print("Waiting for workers...")

    start = time.time()
    timeout = 30

    while len(results) < NUM_JOBS:
        if time.time() - start > timeout:
            print("❌ Timeout waiting for workers")
            break

        r = requests.get(f"{SERVER}/queues/results/messages")

        if r.status_code != 200:
            time.sleep(0.5)
            continue

        data = r.json()

        if "job_id" not in data:
            time.sleep(0.5)
            continue

        job_id = data["job_id"]

        print("Processed:", job_id)
        results.add(job_id)

    print("\nExpected:", job_ids)
    print("Received:", results)

    if results == job_ids:
        print("✅ PASS: Multiple workers processed all jobs correctly")
    else:
        print("❌ FAIL: Missing or duplicate jobs")


# -------------------------
# RUN ALL
# -------------------------
def run_all():
    test_create_queue()
    test_list_queues()
    test_push_pop()
    test_fifo()
    test_queue_not_exist()
    test_queue_full()
    test_worker_flow()
    test_multiple_workers()
    test_thread_safety()
    test_persistence()


if __name__ == "__main__":
    run_all()