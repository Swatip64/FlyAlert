// src/firebase-config.js

import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getMessaging } from 'firebase/messaging';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBb0p9GdUeC9JKGtnOxWNQqlHhLRKN_UJU",
  authDomain: "flightstatusapp-49d34.firebaseapp.com",
  projectId: "flightstatusapp-49d34",
  storageBucket: "flightstatusapp-49d34.appspot.com",
  messagingSenderId: "378544592523",
  appId: "1:378544592523:web:e8b3a4c132793673ba668e",
  measurementId: "G-WNT7HT5Q1C"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Messaging
const messaging = getMessaging(app);

// Initialize Auth and Firestore
const auth = getAuth(app);
const firestore = getFirestore(app);

export { auth, firestore, messaging, firebaseConfig };
