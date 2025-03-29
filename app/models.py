from pydantic import BaseModel

class DetectedPerson(BaseModel):
    """
    This model is used for inbound/outbound JSON data.
    We store lat/long in Firestore as a GeoPoint, but
    still define them as floats here for user input.
    """
    name: str
    latitude: float
    longitude: float