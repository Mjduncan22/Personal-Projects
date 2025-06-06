import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firestore(service_account_key_path):
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
