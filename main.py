import logging
import logging.config

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger(__name__)

from notification_service import NotificationService
from protocol import HealthzedUser

notification_service = NotificationService()


def deliver_ping(from_user: HealthzedUser, to_user: HealthzedUser, message: str):
    notification_service.send_sns_notification(message=message)
    logger.info(f"delivering ping from {from_user.id} to {to_user.id}")
    return True
