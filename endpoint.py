from fastapi import FastAPI
from main import deliver_ping

from protocol import PingRequest, PingResponse

app = FastAPI()


@app.post("/send_ping")
def send_ping(PingRequest):
    from_user = PingRequest.from_user
    to_user = PingRequest.to_user

    deliver_ping.delay(from_user, to_user)

    return PingResponse(status_code=200, message="Ping enqueued successfully!")
