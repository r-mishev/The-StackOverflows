from fastapi import  APIRouter, Request
from twilio.twiml.messaging_response import MessagingResponse
from app.firebase import add_person_to_firestore
from app.pending_data import pending_detections

router = APIRouter()

@router.post("/incoming_sms")
async def handle_sms(request: Request):
    form_data = await request.form()
    print("SMS Came")
    print(form_data)
    print(pending_detections.items())
    from_number = form_data.get('From')
    body = (form_data.get('Body') or "").strip().lower()

    if body == "help":
        # Find the detection_id that matches this phone_number in pending_detections
        # Because multiple detections could be pending for the same phone, 
        # you might need a more robust approach, but here's a simple example:
        detection_id = None
        for d_id, d_data in pending_detections.items():
            if d_data["phone_number"] == from_number:
                detection_id = d_id
                break
        
        if detection_id:
            # We found a pending detection for this phone number
            data = pending_detections.pop(detection_id)
            
            # Actually add them with wants_help=True
            await add_person_to_firestore(detection_id, data, wants_help=True)

            # Construct a TwiML response
            response = MessagingResponse()
            response.message("Thank you for your reply. Help is on the way.")
            print(f"Person {detection_id} replied HELP. Added to DB with wants_help=True.")
            return str(response)
        else:
            # No matching detection found
            response = MessagingResponse()
            response.message("No pending detection found for this number.")
            return str(response)
    else:
        # They didn't reply "HELP"
        response = MessagingResponse()
        response.message("We received your message. Reply 'HELP' if you need assistance.")
        return str(response)
