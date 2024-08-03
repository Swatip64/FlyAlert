// firebase-messaging-sw.js

importScripts('https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.4/firebase-messaging.js');

// Initialize Firebase in the service worker
const firebaseConfig = {
  apiKey: "AIzaSyBb0p9GdUeC9JKGtnOxWNQqlHhLRKN_UJU",
  authDomain: "flightstatusapp-49d34.firebaseapp.com",
  projectId: "flightstatusapp-49d34",
  storageBucket: "flightstatusapp-49d34.appspot.com",
  messagingSenderId: "378544592523",
  appId: "1:378544592523:web:e8b3a4c132793673ba668e",
  measurementId: "G-WNT7HT5Q1C"
};

firebase.initializeApp(firebaseConfig);

// Retrieve an instance of Firebase Messaging so that it can handle background messages.
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('Received background message ', payload);

  // Customize notification here
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: payload.notification.icon
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
