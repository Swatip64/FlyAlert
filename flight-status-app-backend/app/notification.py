from flask import Flask, request, jsonify
import requests
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Path to your service account JSON file
SERVICE_ACCOUNT_PATH = "C:/Users/Lenovo/OneDrive/Documents/Indigo Assignment/flight-status-app-backend/app/credentials/firebase_credentials.json"

# Initialize Firebase Admin SDK
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    try:
        data = request.json
        device_token = data.get('token')
        message_title = data.get('title', 'Default Title')
        message_body = data.get('body', 'Default Body')

        # Construct the message payload
        message = messaging.Message(
            notification=messaging.Notification(
                title=message_title,
                body=message_body,
            ),
            token=device_token,
        )

        # Send the message
        response = messaging.send(message)

        return jsonify({"status": "success", "response": response}), 200

    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
