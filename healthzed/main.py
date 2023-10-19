import logging.config

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger(__name__)

from healthzed.notification_service import NotificationService

notification_service = NotificationService()


async def deliver_ping(message: str, phone_number: str):
    logger.info(f"asynchronously delivering ping to phone number {phone_number}...")
    notification_service.send_pinpoint_sms_notification(
        destination_number=phone_number,
        message=message,
    )
    return True
