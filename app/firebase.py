import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

json_str = os.getenv("SERVICE_ACCOUNT_JSON")
cred_dict = json.loads(json_str)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)
db = firestore.client()
