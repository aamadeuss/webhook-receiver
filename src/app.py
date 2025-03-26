from fastapi import FastAPI, Request
import redis
import json

app = FastAPI()

redis_client = redis.Redis(host="localhost", port=6379, db=0)

@app.post("/webhook")
async def handle_webhook(
    request: Request
):
    payload = await request.json()
    redis_client.lpush("wehook_queue", json.dumps(payload))
    return {
        "status": "Queued"
    }