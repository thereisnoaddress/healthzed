from healthzed.main import deliver_ping
from healthzed.notification_service import NotificationService
from healthzed.protocol import PingRequest, PingResponse

from fastapi import FastAPI, Request
import uvicorn
import time
import aiohttp
import json

TIMEOUT = 60
POLL_INTERVAL = 1


import asyncio
import logging.config

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger(__name__)

app = FastAPI()
notification_service = NotificationService()


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


@app.post("/receive_ping")
async def receive_ping(request: Request):
    message = await request.json()
    response = await notification_service.receive_ping(message)
    return response


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


@app.post("/send_and_wait")
async def send_and_wait(data: PingRequest):
    logger.info(f"Received request to send and wait: {data}")

    # Send the ping
    logger.info(f"Sending ping to {data.phone_number} with message {data.message}")
    send_task = asyncio.create_task(
        deliver_ping(message=data.message, phone_number=data.phone_number)
    )
    await send_task
    logger.info("Ping sent")

    # Wait for a response
    start_time = time.time()
    while True:
        # Check if a message has been received from the phone number
        logger.info(f"Checking for received messages from {data.phone_number}")
        received_message = notification_service.check_received_messages(
            data.phone_number
        )
        logger.info(f"Received message: {received_message}")
        if received_message is not None:
            logger.info(
                f"Received message from {data.phone_number}: {received_message}"
            )
            return {"status": "Message received", "message": received_message}

        # Check if the timeout has been reached
        if time.time() - start_time > TIMEOUT:
            logger.error("Timeout waiting for response")
            return {"status": "Error", "message": "Timeout waiting for response"}

        # Wait before checking again
        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
