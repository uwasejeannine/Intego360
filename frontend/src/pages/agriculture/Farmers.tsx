import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getFarmers,
  createFarmer,
  updateFarmer,
  deleteFarmer,
} from '../../api/agriculture';

const Farmers: React.FC = () => {
  const queryClient = useQueryClient();
  const { data: farmers, isLoading } = useQuery(['farmers'], getFarmers);
  const [modalOpen, setModalOpen] = useState(false);
  const [editFarmer, setEditFarmer] = useState<any | null>(null);
  const [form, setForm] = useState({ name: '', phone: '', gender: '', location: '' });

  const createMutation = useMutation(createFarmer, {
    onSuccess: () => {
      queryClient.invalidateQueries(['farmers']);
      setModalOpen(false);
      setForm({ name: '', phone: '', gender: '', location: '' });
    },
  });
  const updateMutation = useMutation(({ id, data }: any) => updateFarmer(id, data), {
    onSuccess: () => {
      queryClient.invalidateQueries(['farmers']);
      setModalOpen(false);
      setEditFarmer(null);
      setForm({ name: '', phone: '', gender: '', location: '' });
    },
  });
  const deleteMutation = useMutation(deleteFarmer, {
    onSuccess: () => queryClient.invalidateQueries(['farmers']),
  });

  const handleOpenCreate = () => {
    setEditFarmer(null);
    setForm({ name: '', phone: '', gender: '', location: '' });
    setModalOpen(true);
  };
  const handleOpenEdit = (farmer: any) => {
    setEditFarmer(farmer);
    setForm({ name: farmer.name, phone: farmer.phone, gender: farmer.gender, location: farmer.location });
    setModalOpen(true);
  };
  const handleClose = () => {
    setModalOpen(false);
    setEditFarmer(null);
    setForm({ name: '', phone: '', gender: '', location: '' });
  };
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editFarmer) {
      updateMutation.mutate({ id: editFarmer.id, data: form });
    } else {
      createMutation.mutate(form);
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Farmers</h2>
        <button
          onClick={handleOpenCreate}
          className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
        >
          Add Farmer
        </button>
      </div>
      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gender</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                <th className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {farmers?.map((farmer: any) => (
                <tr key={farmer.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.phone}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.gender}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.location}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleOpenEdit(farmer)}
                      className="text-primary-600 hover:text-primary-900 mr-2"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => deleteMutation.mutate(farmer.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {/* Modal for Create/Edit */}
      {modalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-30 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl">
            <h3 className="text-lg font-semibold mb-4">{editFarmer ? 'Edit Farmer' : 'Add Farmer'}</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Phone</label>
                <input
                  type="text"
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Gender</label>
                <select
                  name="gender"
                  value={form.gender}
                  onChange={handleChange}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                >
                  <option value="">Select</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Location</label>
                <input
                  type="text"
                  name="location"
                  value={form.location}
                  onChange={handleChange}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                />
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={handleClose}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
                  disabled={createMutation.isLoading || updateMutation.isLoading}
                >
                  {editFarmer ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Farmers; 