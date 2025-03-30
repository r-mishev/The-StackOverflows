from datetime import datetime
import os
from typing import Any, Dict
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import GeoPoint

from app import manager

my_credentials = {
    "type": "service_account",
    "project_id": "skyguardian-ff27c",
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY").replace(r'\n', '\n'),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(my_credentials)
firebase_admin.initialize_app(cred)
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
