import os
from twilio.rest import Client
import asyncio

from app.firebase import add_person_to_firestore, db
from app.pending_data import pending_detections

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to_phone_number: str, message: str):
    """Send an SMS using Twilio"""
    message = twilio_client.messages.create(
        body=message,
        from_=TWILIO_NUMBER,
        to=to_phone_number,
    )
    return message.sid

async def wait_for_no_response(detection_id: str, timeout: int = 300):
    """
    Wait for 5 minutes. If the user doesn't reply "HELP" in that time,
    add them to Firestore with wants_help=False.
    """

    # Check if still in 'pending_detections' (it might have been removed if the user replied "HELP")
    if detection_id in pending_detections:
        # The user never replied "HELP" in time => wants_help=False
        data = pending_detections.pop(detection_id)

        # Now actually add them to Firestore
        await add_person_to_firestore(detection_id, data)

        print(f"Person {detection_id} did not respond. Added to DB with wants_help=False.")