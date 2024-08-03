import firebase_admin
from firebase_admin import credentials, messaging

# Path to your service account key JSON file
SERVICE_ACCOUNT_KEY_PATH = "C:/Users/Lenovo/OneDrive/Documents/Indigo Assignment/flight-status-app-backend/app/credentials/firebase_credentials.json"

def initialize_firebase():
    """
    Initialize Firebase Admin SDK.
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred)

def upload_flight_data_to_firebase(db_firestore, flight_data):
    for flight in flight_data:
        # Write data to Firestore
        db_firestore.collection('flights').document(str(flight['id'])).set(flight)

def send_push_notification(token, title, body):
    """
    Sends a push notification to a device using Firebase Cloud Messaging (FCM).

    Parameters:
    - token: The device token of the user to whom you want to send the notification.
    - title: The title of the notification.
    - body: The body content of the notification.
    """
    try:
        # Create a message to be sent
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        # Send the message using Firebase Cloud Messaging
        response = messaging.send(message)
        print('Successfully sent message:', response)
    except Exception as e:
        print('Error sending message:', e)

# Ensure Firebase is initialized
initialize_firebase()
