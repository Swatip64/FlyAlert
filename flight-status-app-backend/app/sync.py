from app.utils import fetch_flight_data
from app.firebase_service import upload_flight_data_to_firebase
from firebase_admin import firestore

def sync_postgresql_to_firebase():
    flight_data = fetch_flight_data()
    db_firestore = firestore.client()
    upload_flight_data_to_firebase(db_firestore, flight_data)
    print("Data synchronized to Firebase successfully.")
