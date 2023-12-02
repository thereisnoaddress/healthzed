from healthzed.main import deliver_ping
from healthzed.notification_service import NotificationService
from healthzed.protocol import PingRequest, PingResponse

from fastapi import FastAPI, Request
import uvicorn
import time

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
