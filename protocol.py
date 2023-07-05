import ObjectId
from dataclasses import dataclass


@dataclass
class HealthzedUser:
    id: str
    name: str
    creation_date: str

@dataclass
class PingRequest:
    from_user: HealthzedUser
    to_user: HealthzedUser

@dataclass
class PingResponse:
    status_code: int
    message: str



