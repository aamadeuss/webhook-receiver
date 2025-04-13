from fastapi import FastAPI, Request, Header
from celery import Celery
import json
import yaml
import os

app = FastAPI()
config = yaml.safe_load(open('src/config/settings.yaml'))

REDIS_URL=os.getenv("REDIS_URL")
celery_app=Celery(
    "tasks",
    broker=REDIS_URL
)

@app.get('/health')
async def healthcheck():
    #log here
    return {'status': 'ok'}

@app.post("/webhook")
async def handle_webhook(
    request: Request,
    x_hub_signature: str = Header(None)
):
    payload = await request.body()
    payload_dict = json.loads(payload)
    command = payload_dict.get("comment", {}).get("body")
    if (payload_dict.get("action") == "created" and
        payload_dict.get("issue", {}).get("pull_request") and 
        command in config['commands']):
        celery_app.send_task("tasks.process_webhook", args=[payload, command])
        return {
            "status": "Queued"
        }
    else:
        return {
            "status": ""
        }