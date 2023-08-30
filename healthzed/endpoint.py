from fastapi import FastAPI
from healthzed.main import deliver_ping
import uvicorn

from healthzed.protocol import PingRequest, PingResponse

app = FastAPI()


@app.get("/healthz")
def check_health():
    return True


@app.post("/send_ping")
def send_ping(data: PingRequest):
    response = deliver_ping(
        from_user=data.from_user,
        to_user=data.to_user,
        message=data.message,
        phone_number=data.phone_number,
    )
    if response:
        return PingResponse(status_code=200, message="Ping sent successfully!")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
