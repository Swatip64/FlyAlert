import random
from app import db
from app.models import Flight

def create_mock_data():
    flights = [
        {'flight_number': 'AA101', 'status': 'On Time', 'gate': 'A1', 'arrival_time': '12:00 PM', 'boarding_time': '11:30 AM'},
        {'flight_number': 'BA202', 'status': 'Delayed', 'gate': 'B2', 'arrival_time': '1:00 PM', 'boarding_time': '12:30 PM'},
        {'flight_number': 'CA303', 'status': 'Cancelled', 'gate': 'C3', 'arrival_time': '3:00 PM', 'boarding_time': '2:30 PM'},
    ]

    for flight_data in flights:
        flight = Flight(**flight_data)
        db.session.add(flight)

    db.session.commit()

if __name__ == '__main__':
    db.create_all()
    create_mock_data()
