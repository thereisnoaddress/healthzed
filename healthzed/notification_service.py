import logging.config

import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        # Using a boto3 client to publish using a phone_number
        # otherwise there would be an ARN conflict
        self.sns_client = boto3.client(
            "sns",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
            region_name=os.environ["AWS_REGION"],
        )

    def send_sns_notification(self, phone_number, message="Test SNS message!"):
        try:
            response = self.sns_client.publish(
                PhoneNumber=phone_number, Message=message
            )
            message_id = response["MessageId"]
            logger.info(f"Published message to phone number {phone_number}")
        except ClientError:
            logger.exception(
                f"Couldn't publish message to phone number {phone_number}."
            )
            raise
        else:
            return message_id
