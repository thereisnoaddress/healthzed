from fastapi import FastAPI, Request
from healthzed.main import deliver_ping
import uvicorn
import aiohttp
import json

from healthzed.protocol import PingRequest, PingResponse

import asyncio
import logging.config

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/healthz")
def check_health():
    return True


@app.post("/send_ping")
async def send_ping(data: PingRequest):
    send_task = asyncio.create_task(
        deliver_ping(message=data.message, phone_number=data.phone_number)
    )

    await send_task

    return PingResponse(status_code=200, message="Ping sent successfully!")


@app.post("/sns_endpoint")
async def sns_endpoint(request: Request):
    message = await request.json()
    if "Type" in message and message["Type"] == "SubscriptionConfirmation":
        # handle subscription confirmation
        confirmation_url = message["SubscribeURL"]
        async with aiohttp.ClientSession() as session:
            async with session.get(confirmation_url) as resp:
                print(await resp.text())
    else:
        message = message["Message"]
        # Parse the inner JSON string
        inner_message = json.loads(message)
        # Extract the desired fields
        originationNumber = inner_message["originationNumber"]
        messageBody = inner_message["messageBody"]
        logger.info(f"Received message from {originationNumber}: {messageBody}")
    return {
        "status": "Message received",
        "originationNumber": originationNumber,
        "messageBody": messageBody,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
