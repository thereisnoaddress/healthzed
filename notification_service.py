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
        self.sns_resource = boto3.resource(
            "sns",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
            region_name=os.environ["AWS_REGION"],
        )

        # SNS topic creation is idempotent, so it'll reuse the same topic if exists
        self.sns_topic = self.sns_resource.create_topic(Name="healthzed-test-topic")

    def send_sns_notification(self, message="Test SNS message!"):
        try:
            response = self.sns_topic.publish(Message=message)
            message_id = response["MessageId"]
            logger.info("Published message to topic %s.", self.sns_topic.arn)
        except ClientError:
            logger.exception(
                "Couldn't publish message to topic %s.", self.sns_topic.arn
            )
            raise
        else:
            return message_id
