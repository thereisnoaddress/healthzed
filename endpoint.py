from fastapi import FastAPI
from main import deliver_ping

from protocol import PingRequest, PingResponse

app = FastAPI()

@app.get("/healthz"):
def healthzee():
    return True


@app.post("/send_ping")
def send_ping(from_user, to_user):
    # TODO: add celery queue config
    # deliver_ping.delay(from_user, to_user)
    response = deliver_ping(from_user=from_user, to_user=to_user)
    if response:
        return PingResponse(status_code=200, message="Ping enqueued successfully!")
