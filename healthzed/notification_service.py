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

    async def process_sns_endpoint(self, request):
        message = await request.json()
        if "Type" in message and message["Type"] == "SubscriptionConfirmation":
            # handle subscription confirmation
            confirmation_url = message["SubscribeURL"]
            async with aiohttp.ClientSession() as session:
                async with session.get(confirmation_url) as resp:
                    print(await resp.text())
        else:
            try:
                # Try to parse the inner JSON string
                inner_message = json.loads(message["Message"])
                # Try to parse the SNS Message field
                sns_message = json.loads(
                    inner_message["requestPayload"]["Records"][0]["Sns"]["Message"]
                )
                # Extract the desired fields
                originationNumber = sns_message["originationNumber"]
                messageBody = sns_message["messageBody"]
                logger.info(f"Received message from {originationNumber}: {messageBody}")
                self.numbers_that_replied[originationNumber] = messageBody
                return {
                    "status": "Message received",
                    "originationNumber": originationNumber,
                    "messageBody": messageBody,
                }
            except json.JSONDecodeError:
                return {"status": "Error", "message": "Invalid JSON format"}
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                logger.error(f"Received message: {message}")
                return {"status": "Error processing message", "error": str(e)}
