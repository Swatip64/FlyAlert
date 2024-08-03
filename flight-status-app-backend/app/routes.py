from flask import request, jsonify
from flask_restx import Api, Resource
from app.models import Flight, User, Notification
from app.firebase_service import send_push_notification
from app import socketio

def initialize_routes(api: Api):
    # Define the namespace for organization
    flight_ns = api.namespace('flights', description='Flight operations')
    notification_ns = api.namespace('notifications', description='Notification operations')
    user_ns = api.namespace('users', description='User operations')

    @flight_ns.route('/')
    class FlightList(Resource):
        def get(self):
            flights = Flight.query.all()
            return jsonify([{
                'id': flight.id,
                'flightNumber': flight.flight_number,
                'status': flight.status,
                'gate': flight.gate,
                'arrivalTime': flight.arrival_time,
                'boardingTime': flight.boarding_time
            } for flight in flights])

        def post(self):
            data = request.json
            flight = Flight.create_flight(
                flight_number=data['flightNumber'],
                status=data['status'],
                gate=data.get('gate'),
                arrival_time=data.get('arrivalTime'),
                boarding_time=data.get('boardingTime')
            )
            socketio.emit('flight_updates', [{
                'id': flight.id,
                'flightNumber': flight.flight_number,
                'status': flight.status,
                'gate': flight.gate,
                'arrivalTime': flight.arrival_time,
                'boardingTime': flight.boarding_time
            }], broadcast=True)
            return jsonify({'message': 'Flight created', 'flight': flight}), 201

    @flight_ns.route('/<int:flight_id>')
    class FlightResource(Resource):
        def put(self, flight_id):
            data = request.json
            flight = Flight.update_flight(
                flight_id,
                flight_number=data['flightNumber'],
                status=data['status'],
                gate=data.get('gate'),
                arrival_time=data.get('arrivalTime'),
                boarding_time=data.get('boardingTime')
            )
            socketio.emit('flight_updates', [{
                'id': flight.id,
                'flightNumber': flight.flight_number,
                'status': flight.status,
                'gate': flight.gate,
                'arrivalTime': flight.arrival_time,
                'boardingTime': flight.boarding_time
            }], broadcast=True)
            return jsonify({'message': 'Flight updated', 'flight': flight}), 200

        def delete(self, flight_id):
            Flight.delete_flight(flight_id)
            socketio.emit('flight_deleted', {'id': flight_id}, broadcast=True)
            return jsonify({'message': 'Flight deleted'}), 200

    @notification_ns.route('/')
    class NotificationList(Resource):
        def post(self):
            data = request.json
            notification = Notification.create_notification(
                user_id=data['userId'],
                flight_id=data['flightId'],
                message=data['message'],
                timestamp=data['timestamp']
            )
            user = User.get_user_by_id(data['userId'])
            if user:
                send_push_notification(
                    token=user.notification_preferences.get('deviceToken'),
                    title='Flight Update',
                    body=data['message']
                )
            return jsonify({'message': 'Notification created', 'notification': notification}), 201

    @user_ns.route('/<int:user_id>/notifications')
    class UserNotifications(Resource):
        def get(self, user_id):
            notifications = Notification.get_notifications_by_user(user_id)
            return jsonify([{
                'id': notification.id,
                'userId': notification.user_id,
                'flightId': notification.flight_id,
                'message': notification.message,
                'timestamp': notification.timestamp
            } for notification in notifications])
