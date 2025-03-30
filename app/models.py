from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DetectedPerson(BaseModel):
    """
    This model is used for inbound/outbound JSON data.
    We store lat/long in Firestore as a GeoPoint, but
    still define them as floats here for user input.
    """
    timestamp: Optional[datetime] = None
    id: Optional[str] = None
    latitude: float
    longitude: float
    wants_help: bool = False
