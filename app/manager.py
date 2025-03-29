from typing import List
from fastapi import WebSocket

from app.models import DetectedPerson

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_person_list(self, person_list: list[DetectedPerson]):
        data = [person.model_dump() for person in person_list]
        for connection in self.active_connections:
            await connection.send_json({"type": "all_people", "data": data})

    async def broadcast_new_detection(self, person: DetectedPerson):
        for connection in self.active_connections:
            await connection.send_json({"type": "new_detection", "data": person.model_dump()})

manager = ConnectionManager()