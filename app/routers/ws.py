from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handles WebSocket connections. Keeps the connection alive and manages disconnections.
    Optionally, can send the list of existing detected people upon connection.
    """
    print("🔌 WebSocket client connected")
    await manager.connect(websocket)

    try:
        # Optionally send the list of existing detected people on connect
        # detected_people = load_existing_people_from_firestore()
        # await manager.send_person_list(detected_people)

        # Keep the WebSocket connection alive
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        # Handle WebSocket disconnections
        manager.disconnect(websocket)
        print("❌ WebSocket client disconnected")
