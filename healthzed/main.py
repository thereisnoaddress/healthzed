import logging.config

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger(__name__)

from healthzed.notification_service import NotificationService

notification_service = NotificationService()


def deliver_ping(message: str, phone_number: str):
    logger.info(f"delivering ping to phone number {phone_number}...")
    notification_service.send_sns_notification(
        phone_number=phone_number, message=message
    )
    return True
