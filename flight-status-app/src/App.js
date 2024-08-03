import React from 'react';
import './App.css';
import FlightStatusDashboard from './components/FlightStatusDashboard';
import NotificationsPanel from './components/NotificationsPanel';

const App = () => {
  return (
    <div className="app">
      <header>
        <h1>Flight Status and Notifications System</h1>
      </header>
      <main>
        <FlightStatusDashboard />
        <NotificationsPanel />
      </main>
    </div>
  );
};

export default App;
