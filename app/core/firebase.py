import firebase_admin
from firebase_admin import credentials, firestore

from app.core.config import firebase_settings

cred = credentials.Certificate(firebase_settings.firebase_credentials_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
