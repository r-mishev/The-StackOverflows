import asyncio
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from google.cloud.firestore_v1 import GeoPoint

from app.firebase import db
from app.auth import get_current_user
from app.models import DetectedPerson
from app.twilio import send_sms, wait_for_no_response

from app.pending_data import pending_detections

router = APIRouter()

@router.get("/people", dependencies=[Depends(get_current_user)])
def get_detected_people(current_user: dict = Depends(get_current_user)) -> List[DetectedPerson]:
    """
    Returns a list of detected people for the currently logged-in admin.
    Only people detected by the admin (based on their 'id') are included.
    """
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Admin 'id' not found in current_user")

    detected_people = []
    docs = db.collection("detected_people").stream()
    for doc in docs:
        doc_dict = doc.to_dict()

        # Retrieve Firestore fields
        timestamp = doc_dict.get("timestamp")
        geo_point: GeoPoint = doc_dict.get("location")
        wants_help = doc_dict.get("wants_help")
        detected_by = doc_dict.get("detected_by")
        id=doc_dict.get("id")

        # Include person only if detected by the current admin
        if detected_by == user_id and geo_point:
            detected_people.append(
                DetectedPerson(
                    timestamp=timestamp,
                    wants_help=wants_help,
                    latitude=geo_point.latitude,
                    longitude=geo_point.longitude,
                    id=id
                )
            )

    return detected_people

@router.post("/detect", dependencies=[Depends(get_current_user)])
async def detect_person(person: DetectedPerson, current_user: dict = Depends(get_current_user)):
    """
    1) Generates a detection ID,
    2) Sends an SMS asking the user to reply "HELP" if they need assistance,
    3) Stores detection data in memory for up to 5 minutes,
    4) If no "HELP" after 5 minutes => add doc with wants_help=False,
       If "HELP" arrives => add doc with wants_help=True and cancel wait.
    """

    detection_id = str(uuid.uuid4())
    
    # Acquire admin ID from current_user
    admin_id = current_user.get("id")
    if not admin_id:
        raise HTTPException(status_code=400, detail="Admin 'id' not found in current_user")

    # Prepare data to store in memory
    detection_data = {
        "timestamp": datetime.now(),
        "latitude": person.latitude,
        "longitude": person.longitude,
        "admin_id": admin_id,
        "phone_number": "+359894090404",  # Or person.phone_number if your model includes it
        "wants_help": False,  # default to False
    }
    
    # Store in the in-memory dictionary
    pending_detections[detection_id] = detection_data

    # Send the SMS right away
    send_sms(detection_data["phone_number"], "You now have signal. Reply 'HELP' if you need assistance.")
    
    # Start the 5-minute wait in background
    asyncio.create_task(wait_for_no_response(detection_id, timeout=300))

    # We do NOT add anything to Firestore yet!
    return {"status": "ok", "message": f"Detection started with ID {detection_id}. SMS sent."}
