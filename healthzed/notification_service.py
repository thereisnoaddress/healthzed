import logging.config

import os
import json
import boto3
import aiohttp
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

logging.config.fileConfig("logging.conf")

# create logger
logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.pinpoint_client = boto3.client(
            "pinpoint",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_SECRET_KEY"],
            region_name=os.environ["AWS_PINPOINT_REGION"],
        )

        # dictionary of number to received message
        self.numbers_that_replied = {}

    def send_pinpoint_sms_notification(
        self,
        destination_number,
        message,
        message_type="PROMOTIONAL",
        origination_number="+18078085477",
        app_id="8bd98417d59a452f96fcc2b60cbd13cf",
    ):
        try:
            response = self.pinpoint_client.send_messages(
                ApplicationId=app_id,
                MessageRequest={
                    "Addresses": {destination_number: {"ChannelType": "SMS"}},
                    "MessageConfiguration": {
                        "SMSMessage": {
                            "Body": message,
                            "MessageType": message_type,
                            "OriginationNumber": origination_number,
                        }
                    },
                },
            )
        except ClientError:
            logger.exception("Couldn't send message.")
            raise
        else:
            return response["MessageResponse"]["Result"][destination_number][
                "MessageId"
            ]

    def check_received_messages(self, phone_number):
        if phone_number in self.numbers_that_replied:
            message = self.numbers_that_replied[phone_number]
            del self.numbers_that_replied[phone_number]
            return message
        else:
            return False
