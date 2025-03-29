from typing import List
import json
from fastapi import WebSocket

from app.models import DetectedPerson

class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts messages to active connections.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accepts a WebSocket connection and adds it to the active connections list.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Removes a WebSocket connection from the active connections list.
        """
        self.active_connections.remove(websocket)

    async def send_person_list(self, person_list: List[DetectedPerson]):
        """
        Sends the list of detected persons to all active WebSocket connections.
        """
        data = [person.model_dump() for person in person_list]
        for connection in self.active_connections:
            await connection.send_json({"type": "all_people", "data": json.loads(data.model_dump_json())})

    async def broadcast_new_detection(self, person: DetectedPerson):
        """
        Sends new detection data to all active WebSocket connections.
        """
        for connection in self.active_connections:
            await connection.send_json({"type": "new_detection", "data": json.loads(person.model_dump_json())})

# Create a manager instance for managing WebSocket connections
manager = ConnectionManager()
