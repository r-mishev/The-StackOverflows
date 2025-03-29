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
        geo_point: GeoPoint = doc_dict.get("location")
        name = doc_dict.get("name")
        if geo_point:
            detected_people.append(
                DetectedPerson(
                    name=name,
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
    geo_point = GeoPoint(person.latitude, person.longitude)
    data = {
        "name": person.name,
        "location": geo_point
    }
    # Use person's name as the Firestore doc ID
    db.collection("detected_people").document(person.name).set(data)

    # Broadcast to all WebSocket clients
    await manager.broadcast_new_detection(person)

    return {"status": "ok", "message": "Person detected and broadcasted"}
