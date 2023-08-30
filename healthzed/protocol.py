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
    message: str
    phone_number: str


@dataclass
class PingResponse:
    status_code: int
    message: str