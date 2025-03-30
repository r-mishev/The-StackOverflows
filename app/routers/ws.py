from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.manager import manager
from app.firebase import db
from app.models import DetectedPerson

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("🔌 WebSocket client connected")
    await manager.connect(websocket)

    try:
        # Optional: send list of existing people on connect
        #detected_people = load_existing_people_from_firestore()
        #await manager.send_person_list(detected_people)

        # Keep connection alive
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("❌ WebSocket client disconnected")
