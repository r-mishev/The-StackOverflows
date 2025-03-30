from datetime import datetime
import os
from typing import Any, Dict
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import GeoPoint

from app import manager

# Set up the path to the service account key
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, 'serviceAccountKey.json')

# Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

def add_person_to_firestore(detection_id: str, data: Dict[str, Any], wants_help: bool) -> None:
    """
    Creates a Firestore document with the final wants_help status
    and broadcasts the new detection data over WebSocket if needed.

    Args:
        detection_id (str): A unique ID representing this detection session.
        data (Dict[str, Any]): The detection data to be stored (e.g. timestamp, lat/lon, admin_id).
        wants_help (bool): Whether the person has indicated they want help.

    Returns:
        None
    """
    # Build the Firestore doc
    doc_data = {
        "timestamp": data.get("timestamp", datetime.now()),
        "location": GeoPoint(
            data["latitude"],
            data["longitude"]
        ) if ("latitude" in data and "longitude" in data) else None,
        "wants_help": wants_help,
        "id": detection_id,
        "detected_by": data.get("admin_id"),
        # Add any other fields from your data dict if needed, e.g. phone_number, fcm_token, etc.
        # "phone_number": data.get("phone_number"),
    }

    # Create or overwrite the Firestore document
    db.collection("detected_people").document(detection_id).set(doc_data)

    # Broadcast the new detection to any WebSocket clients
    manager.broadcast_new_detection(doc_data)

    print(f"Added detection record {detection_id} to Firestore with wants_help={wants_help} and broadcasted it.")
