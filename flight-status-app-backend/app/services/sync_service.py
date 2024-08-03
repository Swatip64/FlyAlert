from app import db
from app.models import Flight
from app.firebase_service import db_firestore

def upload_flight_data_to_firebase(flight_data):
    for flight in flight_data:
        # Write data to Firestore
        db_firestore.collection('flights').document(str(flight['id'])).set(flight)
def fetch_flight_data():
    with db.session() as session:
        flights = session.query(Flight).all()
        flight_data = [
            {
                'id': flight.id,
                'flightNumber': flight.flight_number,
                'status': flight.status,
                'gate': flight.gate,
                'arrivalTime': flight.arrival_time.isoformat(),
                'boardingTime': flight.boarding_time.isoformat()
            }
            for flight in flights
        ]
    return flight_data
