from fastapi import FastAPI, Request
import redis
import json
import os

app = FastAPI()

REDIS_URL=os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

@app.get('/health')
async def healthcheck():
    #log here
    return {'status': 'ok'}

@app.post("/webhook")
async def handle_webhook(
    request: Request
):
    payload = await request.json()
    redis_client.lpush("wehook_queue", json.dumps(payload))
    return {
        "status": "Queued"
    }