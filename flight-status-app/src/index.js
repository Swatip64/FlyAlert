import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/App.css'; // Custom styles
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS
import App from './App';
import { getMessaging, getToken, onMessage } from 'firebase/messaging';
import { initializeApp } from 'firebase/app';
import { firebaseConfig } from './firebase-config';

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

// VAPID key for FCM
const VAPID_KEY = 'BBA4c7wzHiOe90p1mmnTGQHeb7Td6N363N1VB1VuwVf_yFIVOB2F1OA3kK0WF00STSRKkwN6hBm08pgI_N9DOJM';

// Request permission to receive notifications
const requestNotificationPermission = async () => {
  try {
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      console.log('Notification permission granted.');
      // Get the device token
      getDeviceToken();
    } else {
      console.log('Unable to get permission to notify.');
    }
  } catch (error) {
    console.error('Error requesting notification permission:', error);
  }
};

// Function to get the device token
const getDeviceToken = async () => {
  try {
    const token = await getToken(messaging, { vapidKey: VAPID_KEY });
    if (token) {
      console.log('Device token:', token);
      // Send the token to your server and store it for later use
      sendTokenToServer(token);
    } else {
      console.log('No registration token available. Request permission to generate one.');
    }
  } catch (error) {
    console.error('An error occurred while retrieving token. ', error);
  }
};

// Send the device token to the server
const sendTokenToServer = async (token) => {
  try {
    const response = await fetch('/send-notification', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token }),
    });

    if (response.ok) {
      console.log('Token successfully sent to the server');
    } else {
      console.error('Failed to send token to server');
    }
  } catch (error) {
    console.error('Error sending token to server:', error);
  }
};

// Listen for incoming messages while the app is in the foreground
onMessage(messaging, (payload) => {
  console.log('Message received. ', payload);
  // Display an alert or custom notification
  alert(`Notification: ${payload.notification.title} - ${payload.notification.body}`);
});

// Request notification permission on page load
requestNotificationPermission();

// Register the service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/firebase-messaging-sw.js')
    .then((registration) => {
      console.log('Service Worker registered with scope:', registration.scope);
    })
    .catch((error) => {
      console.error('Service Worker registration failed:', error);
    });
}

// Create root and render the app
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
