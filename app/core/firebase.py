import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import Client

from app.core.config import firebase_settings

cred = credentials.Certificate(firebase_settings.firebase_credentials_path)
firebase_admin.initialize_app(cred)

client = firestore.client()


def get_firebase_client() -> Client:
    return client
