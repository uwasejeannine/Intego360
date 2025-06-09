import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getFarmers,
  createFarmer,
  updateFarmer,
  deleteFarmer,
  getFarmerStats,
  getFarmerProductionHistory,
} from '../../api/agriculture';
import type { Farmer } from '../../api/agriculture';

const Farmers: React.FC = () => {
  const queryClient = useQueryClient();
  const { data: farmers, isLoading } = useQuery({
    queryKey: ['farmers'],
    queryFn: getFarmers,
  });
  const [modalOpen, setModalOpen] = useState(false);
  const [editFarmer, setEditFarmer] = useState<Farmer | null>(null);
  const [form, setForm] = useState<Partial<Farmer>>({
    farmer_id: '',
    first_name: '',
    last_name: '',
    national_id: '',
    date_of_birth: '',
    gender: 'M',
    phone_number: '',
    email: '',
    district: 0,
    sector: 0,
    cell: '',
    village: '',
    total_land_hectares: 0,
    farming_experience_years: 0,
    education_level: 'primary',
    main_crops: [],
    is_cooperative_member: false,
    cooperative_name: '',
    has_bank_account: false,
    bank_name: '',
    account_number: '',
  });

  const createMutation = useMutation({
    mutationFn: createFarmer,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
      setModalOpen(false);
      resetForm();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Farmer> }) => updateFarmer(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
      setModalOpen(false);
      setEditFarmer(null);
      resetForm();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteFarmer,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['farmers'] }),
  });

  const resetForm = () => {
    setForm({
      farmer_id: '',
      first_name: '',
      last_name: '',
      national_id: '',
      date_of_birth: '',
      gender: 'M',
      phone_number: '',
      email: '',
      district: 0,
      sector: 0,
      cell: '',
      village: '',
      total_land_hectares: 0,
      farming_experience_years: 0,
      education_level: 'primary',
      main_crops: [],
      is_cooperative_member: false,
      cooperative_name: '',
      has_bank_account: false,
      bank_name: '',
      account_number: '',
    });
  };

  const handleOpenCreate = () => {
    setEditFarmer(null);
    resetForm();
    setModalOpen(true);
  };

  const handleOpenEdit = (farmer: Farmer) => {
    setEditFarmer(farmer);
    setForm({
      farmer_id: farmer.farmer_id,
      first_name: farmer.first_name,
      last_name: farmer.last_name,
      national_id: farmer.national_id,
      date_of_birth: farmer.date_of_birth,
      gender: farmer.gender,
      phone_number: farmer.phone_number,
      email: farmer.email,
      district: farmer.district,
      sector: farmer.sector,
      cell: farmer.cell,
      village: farmer.village,
      total_land_hectares: farmer.total_land_hectares,
      farming_experience_years: farmer.farming_experience_years,
      education_level: farmer.education_level,
      main_crops: farmer.main_crops,
      is_cooperative_member: farmer.is_cooperative_member,
      cooperative_name: farmer.cooperative_name,
      has_bank_account: farmer.has_bank_account,
      bank_name: farmer.bank_name,
      account_number: farmer.account_number,
    });
    setModalOpen(true);
  };

  const handleClose = () => {
    setModalOpen(false);
    setEditFarmer(null);
    resetForm();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setForm((prev: Partial<Farmer>) => ({
      ...prev,
      [name]: type === 'number' ? Number(value) : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editFarmer) {
      updateMutation.mutate({ id: editFarmer.id, data: form });
    } else {
      createMutation.mutate(form as Farmer);
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
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phone</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gender</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Land (ha)</th>
                <th className="px-6 py-3"></th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {farmers?.map((farmer: Farmer) => (
                <tr key={farmer.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.farmer_id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {farmer.first_name} {farmer.last_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.phone_number}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.gender}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {farmer.village}, {farmer.cell}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{farmer.total_land_hectares}</td>
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
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl shadow-xl">
            <h3 className="text-lg font-semibold mb-4">{editFarmer ? 'Edit Farmer' : 'Add Farmer'}</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Farmer ID</label>
                  <input
                    type="text"
                    name="farmer_id"
                    value={form.farmer_id}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">National ID</label>
                  <input
                    type="text"
                    name="national_id"
                    value={form.national_id}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">First Name</label>
                  <input
                    type="text"
                    name="first_name"
                    value={form.first_name}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Last Name</label>
                  <input
                    type="text"
                    name="last_name"
                    value={form.last_name}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Date of Birth</label>
                  <input
                    type="date"
                    name="date_of_birth"
                    value={form.date_of_birth}
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
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Phone Number</label>
                  <input
                    type="tel"
                    name="phone_number"
                    value={form.phone_number}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">District</label>
                  <input
                    type="number"
                    name="district"
                    value={form.district}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Sector</label>
                  <input
                    type="number"
                    name="sector"
                    value={form.sector}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Cell</label>
                  <input
                    type="text"
                    name="cell"
                    value={form.cell}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Village</label>
                  <input
                    type="text"
                    name="village"
                    value={form.village}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Total Land (hectares)</label>
                  <input
                    type="number"
                    name="total_land_hectares"
                    value={form.total_land_hectares}
                    onChange={handleChange}
                    required
                    min="0"
                    step="0.01"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Farming Experience (years)</label>
                  <input
                    type="number"
                    name="farming_experience_years"
                    value={form.farming_experience_years}
                    onChange={handleChange}
                    required
                    min="0"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Education Level</label>
                  <select
                    name="education_level"
                    value={form.education_level}
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  >
                    <option value="none">No formal education</option>
                    <option value="primary">Primary education</option>
                    <option value="secondary">Secondary education</option>
                    <option value="vocational">Vocational training</option>
                    <option value="university">University education</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Cooperative Member</label>
                  <div className="mt-2">
                    <label className="inline-flex items-center">
                      <input
                        type="checkbox"
                        name="is_cooperative_member"
                        checked={form.is_cooperative_member}
                        onChange={(e) => setForm((prev: Partial<Farmer>) => ({ ...prev, is_cooperative_member: e.target.checked }))}
                        className="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      />
                      <span className="ml-2">Yes</span>
                    </label>
                  </div>
                </div>
                {form.is_cooperative_member && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Cooperative Name</label>
                    <input
                      type="text"
                      name="cooperative_name"
                      value={form.cooperative_name}
                      onChange={handleChange}
                      className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    />
                  </div>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700">Has Bank Account</label>
                  <div className="mt-2">
                    <label className="inline-flex items-center">
                      <input
                        type="checkbox"
                        name="has_bank_account"
                        checked={form.has_bank_account}
                        onChange={(e) => setForm((prev: Partial<Farmer>) => ({ ...prev, has_bank_account: e.target.checked }))}
                        className="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      />
                      <span className="ml-2">Yes</span>
                    </label>
                  </div>
                </div>
                {form.has_bank_account && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Bank Name</label>
                      <input
                        type="text"
                        name="bank_name"
                        value={form.bank_name}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Account Number</label>
                      <input
                        type="text"
                        name="account_number"
                        value={form.account_number}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      />
                    </div>
                  </>
                )}
              </div>
              <div className="flex justify-end space-x-2 mt-6">
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
                  disabled={createMutation.isPending || updateMutation.isPending}
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