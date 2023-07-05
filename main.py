import logging

logger = logging.getLogger()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    return f"Hi, {name}"


def deliver_ping(from_user, to_user):
    # TODO: add some sort of message delivery service? like AWS SNS
    logger.info(f"delivering ping from {from_user} to {to_user}")
    return True
