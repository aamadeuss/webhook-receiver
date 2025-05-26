from fastapi import FastAPI, Request, Header, HTTPException
import httpx
import json
import yaml
import os

app = FastAPI()
config = yaml.safe_load(open('src/config/settings.yaml'))

APP_URL=os.getenv("APP_URL")

@app.get('/health')
async def healthcheck():
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

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=APP_URL, json={'payload': payload_dict, 'command': command})
                if response.status_code==200:
                    return {
                        "status": "Queued"
                    }
                else:
                    return {
                        "status": "Bad response"
                    }
        except:
            return {
                "status": "Could not connect to app"
            }
    else:
        raise HTTPException(status_code=400, detail="Not called")