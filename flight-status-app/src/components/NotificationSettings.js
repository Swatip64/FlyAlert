import React, { useState } from 'react';

function NotificationSettings() {
  const [notificationSettings, setNotificationSettings] = useState({
    sms: false,
    email: false,
    push: false,
  });

  const handleToggle = (type) => {
    setNotificationSettings({ ...notificationSettings, [type]: !notificationSettings[type] });
  };

  // Add logic to save notification settings (e.g., send to backend)

  return (
    <div className="notification-settings">
      <h2>Notification Settings</h2>
      <label>
        <input
          type="checkbox"
          checked={notificationSettings.sms}
          onChange={() => handleToggle('sms')}
        />
        SMS Notifications
      </label>
      <label>
        <input
          type="checkbox"
          checked={notificationSettings.email}
          onChange={() => handleToggle('email')}
        />
        Email Notifications
      </label>
      <label>
        <input
          type="checkbox"
          checked={notificationSettings.push}
          onChange={() => handleToggle('push')}
        />
        Push Notifications
      </label>
    </div>
  );
}

export default NotificationSettings;
