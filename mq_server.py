
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from message_queue import MessageQueueManager
import uvicorn
from pydantic import BaseModel

app = FastAPI()
manager = MessageQueueManager()


class Message(BaseModel):
    job_id: int
    image: str




@app.get("/health")
def health_check():
    return {"message": "healthy!"}




@app.post("/queues/{name}")
def create_queue(name: str):
    try: 
        manager.create_queue(name)
        return {"message": "Queue sucesfully created!"}
    except Exception as e: 
        return JSONResponse(
            status_code=409,
            content={"error": str(e)}
        )



@app.delete("/queues/{name}")
def delete_queue(name: str):
    try: 
        manager.delete_queue(name)
        return {"message": "Queue deleted sucesfully!"}
    except Exception as e: 
        return JSONResponse(
            status_code=409,
            content={"error": str(e)}
        )



@app.get("/queues")
def list_queues():
    try: 
        queues = manager.list_queues()
        return {"queues": list(queues)}
    except Exception as e: 
        return JSONResponse(
            status_code=409,
            content={"error": str(e)}
        )



@app.post("/queues/{name}/messages")
def push_to_queue(name: str, message: Message):
    try: 
        manager.push(name, message)
        return {"message": f"[{str(message.image)}] added sucesfully to queue]!"}
    except Exception as e: 
        return JSONResponse(
            status_code=409,
            content={"error": str(e)}
        )




@app.get("/queues/{name}/messages")
def pop_from_queue(name: str):
    try: 
        return manager.pop(name)
    except Exception as e: 
        return JSONResponse(
            status_code=409,
            content={"error": str(e)}
        )



@app.get("/get_queue_content/{name}")
def get_queue_content(name: str):
    try: 
        messages = manager.get_queue_content(name)
        return {"messages": messages}
    except Exception as e: 
        return JSONResponse(
            status_code=409,
            content={"error": str(e)}
        )










if __name__ == "__main__":
    uvicorn.run("mq_server:app", host="0.0.0.0", port=8000, reload=True)





























