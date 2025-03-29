from datetime import datetime
import uuid
import json
from fastapi import APIRouter, Depends
from typing import List

from google.cloud.firestore_v1 import GeoPoint

from app.firebase import db
from app.auth import get_current_user
from app.models import DetectedPerson
from app.manager import ConnectionManager

from app.manager import manager

router = APIRouter()

@router.get("/people", dependencies=[Depends(get_current_user)])
def get_detected_people() -> List[DetectedPerson]:
    """
    Protected endpoint: returns the entire list of detected people from Firestore.
    Firestore stores location as a GeoPoint.
    """
    detected_people = []
    docs = db.collection("detected_people").stream()
    for doc in docs:
        doc_dict = doc.to_dict()
        # doc_dict["location"] is a GeoPoint
        timestamp = doc_dict.get("timestamp")
        geo_point: GeoPoint = doc_dict.get("location")
        wants_help = doc_dict.get("wants_help")
        if geo_point:
            detected_people.append(
                DetectedPerson(
                    timestamp=timestamp,
                    wants_help=wants_help,
                    latitude=geo_point.latitude,
                    longitude=geo_point.longitude
                )
            )
    return detected_people

@router.post("/detect", dependencies=[Depends(get_current_user)])
async def detect_person(person: DetectedPerson):
    """
    Protected endpoint: adds a newly detected person to Firestore as a GeoPoint
    and broadcasts it to all WebSocket connections.
    """
    document_id = str(uuid.uuid4())

    person.timestamp = datetime.now()
    person.id=document_id
    geo_point = GeoPoint(person.latitude, person.longitude)

    data = {
        "timestamp": person.timestamp,
        "wants_help": person.wants_help,
        "location": geo_point,
        "id":document_id
    }
    # Use person's name as the Firestore doc ID
    db.collection("detected_people").document(document_id).set(data)

    # Broadcast to all WebSocket clients
    await manager.broadcast_new_detection(person)

    return {"status": "ok", "message": "Person detected and broadcasted"}