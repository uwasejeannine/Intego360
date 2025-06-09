// Settings.tsx
import React, { useState } from 'react';

const Settings: React.FC = () => {
  const [notifications, setNotifications] = useState({
    email: true,
    sms: false,
    push: true,
  });
  const [language, setLanguage] = useState('en');
  const [showDeactivate, setShowDeactivate] = useState(false);

  const handleNotifChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNotifications({ ...notifications, [e.target.name]: e.target.checked });
  };

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(e.target.value);
  };

  const handleDeactivate = () => {
    setShowDeactivate(true);
  };

  const handleConfirmDeactivate = () => {
    // Integrate with backend here
    setShowDeactivate(false);
    alert('Account deactivated (mock)');
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow mt-8">
      <h2 className="text-2xl font-bold mb-6">Settings</h2>
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2">Notification Preferences</h3>
        <div className="space-y-2">
          <label className="flex items-center">
            <input type="checkbox" name="email" checked={notifications.email} onChange={handleNotifChange} className="mr-2" />
            Email Notifications
          </label>
          <label className="flex items-center">
            <input type="checkbox" name="sms" checked={notifications.sms} onChange={handleNotifChange} className="mr-2" />
            SMS Notifications
          </label>
          <label className="flex items-center">
            <input type="checkbox" name="push" checked={notifications.push} onChange={handleNotifChange} className="mr-2" />
            Push Notifications
          </label>
        </div>
      </div>
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2">Language</h3>
        <select
          value={language}
          onChange={handleLanguageChange}
          className="block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
        >
          <option value="en">English</option>
          <option value="fr">French</option>
          <option value="rw">Kinyarwanda</option>
        </select>
      </div>
      <div>
        <h3 className="text-lg font-semibold mb-2">Account Management</h3>
        <button
          onClick={handleDeactivate}
          className="px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200"
        >
          Deactivate Account
        </button>
        {showDeactivate && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded">
            <p className="mb-2 text-red-700">Are you sure you want to deactivate your account? This action cannot be undone.</p>
            <button
              onClick={handleConfirmDeactivate}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 mr-2"
            >
              Yes, Deactivate
            </button>
            <button
              onClick={() => setShowDeactivate(false)}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings;