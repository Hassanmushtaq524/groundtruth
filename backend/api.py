# api.py
from fastapi import FastAPI, Request
import json

# Create FastAPI instance
app = FastAPI()

@app.get("/")
async def hello_world():
    return {"Message":"hello!"}

# Webhook endpoint to listen for POST requests
@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()  # Parse the JSON payload from webhook
    print("Webhook received:", json.dumps(payload, indent=2))  # For debugging

    # You can add custom logic here to handle the webhook data
    # For example: check event type, update database, trigger actions, etc.

    return {"message": "Webhook received!"}
