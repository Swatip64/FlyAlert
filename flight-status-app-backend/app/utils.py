import os
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
from threading import Thread
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from .env file
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")

# Path to your Firebase service account key
firebase_cred_path = "C:/Users/Lenovo/OneDrive/Documents/Indigo Assignment/flight-status-app-backend/app/credentials/firebase_credentials.json"

def create_app():
    app = Flask(__name__, static_folder='../flight-status-app/build', static_url_path='')
    CORS(app)  # Enable Cross-Origin Resource Sharing

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:1234@localhost/flight_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Import models to register with SQLAlchemy
    from app.models import Flight, Notification, User

    # Initialize Firebase
    cred = credentials.Certificate(firebase_cred_path)
    firebase_admin.initialize_app(cred)

    # Access Firestore
    db_firestore = firestore.client()

    # Initialize Flask-RESTful API
    from flask_restful import Api
    api = Api(app)

    # Register routes
    from app.routes import initialize_routes
    initialize_routes(api)

    # Start the RabbitMQ consumer
    from app.services.notification_service import consume_notifications
    consumer_thread = Thread(target=consume_notifications)
    consumer_thread.start()

    # Define WebSocket events
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')
        # Example of sending initial data
        emit('flight_updates', [{'id': 1, 'flightNumber': 'AA123', 'status': 'On Time', 'gate': 'A1', 'arrivalTime': '2024-07-29T15:00:00', 'boardingTime': '2024-07-29T14:30:00'}])

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('update_flights')
    def handle_update_flights(data):
        # This could be a placeholder for real update logic
        emit('flight_updates', data, broadcast=True)

    # Serve React app
    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/api/flight-status', methods=['GET'])
    def get_flight_status():
        # Replace this with your actual logic
        return jsonify([{'id': 1, 'flightNumber': 'AA123', 'status': 'On Time', 'gate': 'A1', 'arrivalTime': '2024-07-29T15:00:00', 'boardingTime': '2024-07-29T14:30:00'},])

    @app.route('/api/notifications', methods=['GET'])
    def get_notifications():
        # Replace this with your actual logic
        return jsonify({'notifications': ['Flight delayed', 'Gate change']})

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
