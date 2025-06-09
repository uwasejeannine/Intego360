import React, { useState } from 'react';

const mockUser = {
  full_name: 'J Uwase',
  email: 'juwase@email.com',
  phone: '+250 788 123 456',
  role: 'District Officer',
};

const Profile: React.FC = () => {
  const [user, setUser] = useState(mockUser);
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState(user);
  const [showPassword, setShowPassword] = useState(false);
  const [passwords, setPasswords] = useState({ current: '', new: '', confirm: '' });

  const handleEdit = () => setEditMode(true);
  const handleCancel = () => { setEditMode(false); setForm(user); };
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSave = () => {
    setUser(form);
    setEditMode(false);
    // Integrate with backend here
  };
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPasswords({ ...passwords, [e.target.name]: e.target.value });
  };
  const handlePasswordSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Integrate with backend here
    setPasswords({ current: '', new: '', confirm: '' });
    setShowPassword(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow mt-8">
      <h2 className="text-2xl font-bold mb-6">Profile</h2>
      <div className="flex items-center mb-6">
        <div className="h-16 w-16 rounded-full bg-green-200 text-green-700 flex items-center justify-center text-2xl font-bold mr-4">
          {user.full_name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
        </div>
        <div>
          <div className="text-lg font-semibold">{user.full_name}</div>
          <div className="text-gray-500 text-sm">{user.role}</div>
        </div>
      </div>
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2">Personal Information</h3>
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700">Full Name</label>
            <input
              type="text"
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              disabled={!editMode}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 disabled:bg-gray-100"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              disabled={!editMode}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 disabled:bg-gray-100"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Phone</label>
            <input
              type="text"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              disabled={!editMode}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 disabled:bg-gray-100"
            />
          </div>
        </div>
        <div className="mt-4 flex space-x-2">
          {!editMode ? (
            <button onClick={handleEdit} className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700">Edit</button>
          ) : (
            <>
              <button onClick={handleSave} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Save</button>
              <button onClick={handleCancel} className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Cancel</button>
            </>
          )}
        </div>
      </div>
      <div>
        <h3 className="text-lg font-semibold mb-2">Change Password</h3>
        {!showPassword ? (
          <button onClick={() => setShowPassword(true)} className="px-4 py-2 bg-primary-100 text-primary-700 rounded hover:bg-primary-200">Change Password</button>
        ) : (
          <form onSubmit={handlePasswordSubmit} className="space-y-3 mt-2">
            <div>
              <label className="block text-sm font-medium text-gray-700">Current Password</label>
              <input
                type="password"
                name="current"
                value={passwords.current}
                onChange={handlePasswordChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">New Password</label>
              <input
                type="password"
                name="new"
                value={passwords.new}
                onChange={handlePasswordChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Confirm New Password</label>
              <input
                type="password"
                name="confirm"
                value={passwords.confirm}
                onChange={handlePasswordChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                required
              />
            </div>
            <div className="flex space-x-2">
              <button type="submit" className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700">Save</button>
              <button type="button" onClick={() => setShowPassword(false)} className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Cancel</button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default Profile; 