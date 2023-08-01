import logging
import logging.config
logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger(__name__)

def deliver_ping(from_user, to_user):
    # TODO: add some sort of message delivery service? like AWS SNS
    logger.info(f"delivering ping from {from_user} to {to_user}")
    return True
