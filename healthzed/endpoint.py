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
        try:
            # Try to parse the inner JSON string
            inner_message = json.loads(message["Message"])
            # Try to parse the SNS Message field
            sns_message = json.loads(
                inner_message["requestPayload"]["Records"][0]["Sns"]["Message"]
            )
            # Extract the desired fields
            originationNumber = sns_message["originationNumber"]
            messageBody = sns_message["messageBody"]
            logger.info(f"Received message from {originationNumber}: {messageBody}")
            return {
                "status": "Message received",
                "originationNumber": originationNumber,
                "messageBody": messageBody,
            }
        except json.JSONDecodeError:
            return {"status": "Error", "message": "Invalid JSON format"}
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            logger.error(f"Received message: {message}")
            return {"status": "Error processing message", "error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
