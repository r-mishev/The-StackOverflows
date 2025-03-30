import os
import firebase_admin
from firebase_admin import credentials, firestore

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
