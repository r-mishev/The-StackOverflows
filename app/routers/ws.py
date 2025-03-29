from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.firebase import db
from app.manager import ConnectionManager
from app.models import DetectedPerson

from app.manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket for real-time updates of new detections.
    """
    await manager.connect(websocket)
    try:
        # Load existing people from Firestore as a list of DetectedPerson
        detected_people = []
        docs = db.collection("detected_people").stream()
        for doc in docs:
            doc_dict = doc.to_dict()
            detected_by = doc_dict.get("detected_by")
            timestamp = doc_dict.get("timestamp")
            geo_point = doc_dict.get("location")
            wants_help = doc_dict.get("wants_help")
            if detected_by and timestamp and geo_point and wants_help:
                detected_people.append(
                    DetectedPerson(
                        detected_by=detected_by,
                        timestamp=timestamp,
                        wants_help=wants_help,
                        latitude=geo_point.latitude,
                        longitude=geo_point.longitude
                    )
                )

        # Send the entire list to the newly connected client
        await manager.send_person_list(detected_people)

        while True:
            # If the client sends messages, handle them here
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
