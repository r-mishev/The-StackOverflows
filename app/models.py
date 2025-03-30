from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DetectedPerson(BaseModel):
    """
    Model representing a detected person with geolocation and help request status.
    This model is used for inbound/outbound JSON data.
    Latitude and longitude are stored as GeoPoint in Firestore but defined as floats here.
    """
    timestamp: Optional[datetime] = None
    id: Optional[str] = None
    latitude: float
    longitude: float
    wants_help: bool = False
