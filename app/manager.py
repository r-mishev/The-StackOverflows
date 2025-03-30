import json
from typing import List, Union
from fastapi import WebSocket
from app.models import DetectedPerson

class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts messages to active clients.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        Accepts and stores a new WebSocket connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Removes a WebSocket connection from the active connections list.
        """
        self.active_connections.remove(websocket)

    async def send_person_list(self, person_list: List[DetectedPerson]) -> None:
        """
        Broadcasts the complete list of detected persons to all connected WebSocket clients.
        
        Args:
            person_list (List[DetectedPerson]): The list of detected persons.
        """
        # Convert each DetectedPerson instance to a dictionary
        data = [person.model_dump() for person in person_list]
        for connection in self.active_connections:
            # Send the list using JSON (data is already serializable)
            await connection.send_json({"type": "all_people", "data": data})

    async def broadcast_new_detection(self, detection_data: Union[DetectedPerson, dict]) -> None:
        """
        Broadcasts new detection data to all connected WebSocket clients.
        
        Args:
            detection_data (Union[DetectedPerson, dict]): The new detection data.
                If a DetectedPerson instance is provided, it will be converted to a dict.
        """
        # If detection_data is a DetectedPerson, convert it to a dict.
        if isinstance(detection_data, DetectedPerson):
            detection_data = detection_data.model_dump()
        # Otherwise, assume detection_data is already a dict.
        for connection in self.active_connections:
            await connection.send_json({"type": "new_detection", "data": detection_data})

# Create a global instance of the ConnectionManager for use across the app.
manager = ConnectionManager()
