import React, { useState, useEffect } from 'react';

const NotificationsPanel = () => {
  const [notifications, setNotifications] = useState([]);
  const [preferences, setPreferences] = useState({
    sms: true,
    email: true,
    app: true,
  });

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await fetch('/api/notifications');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setNotifications(data.notifications || []);
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }
    };

    fetchNotifications();
  }, []);

  const handlePreferenceChange = (type) => {
    setPreferences((prev) => ({
      ...prev,
      [type]: !prev[type],
    }));
  };

  return (
    <div className="notifications-panel">
      <h2>Notifications</h2>
      <div className="notification-settings">
        <label>
          <input
            type="checkbox"
            checked={preferences.sms}
            onChange={() => handlePreferenceChange('sms')}
          />
          SMS
        </label>
        <label>
          <input
            type="checkbox"
            checked={preferences.email}
            onChange={() => handlePreferenceChange('email')}
          />
          Email
        </label>
        <label>
          <input
            type="checkbox"
            checked={preferences.app}
            onChange={() => handlePreferenceChange('app')}
          />
          App
        </label>
      </div>
      <div className="notification-list">
        <ul>
          {notifications.length > 0 ? (
            notifications.map((notification, index) => (
              <li key={index}>{notification}</li>
            ))
          ) : (
            <p>No notifications available</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default NotificationsPanel;
