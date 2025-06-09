// Education.tsx
import React, { useState } from 'react';
import {
  AcademicCapIcon,
  UsersIcon,
  BuildingLibraryIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts';

const Education: React.FC = () => {
  const [selectedLevel, setSelectedLevel] = useState('all');
  const [selectedMetric, setSelectedMetric] = useState('enrollment');

  // Mock data
  const overviewStats = {
    schools: 142,
    students: 89420,
    teachers: 2840,
    classrooms: 3250,
  };

  const enrollmentData = [
    { level: 'Pre-Primary', enrolled: 8450, target: 12000, rate: 24.2 },
    { level: 'Primary', enrolled: 65200, target: 68000, rate: 95.9 },
    { level: 'Lower Secondary', enrolled: 12800, target: 15000, rate: 85.3 },
    { level: 'Upper Secondary', enrolled: 7200, target: 9000, rate: 80.0 },
    { level: 'TVET', enrolled: 2100, target: 3500, rate: 60.0 },
  ];

  const performanceData = [
    { subject: 'Kinyarwanda', pass_rate: 87.3, national_avg: 84.2 },
    { subject: 'English', pass_rate: 78.9, national_avg: 76.8 },
    { subject: 'French', pass_rate: 72.1, national_avg: 69.5 },
    { subject: 'Mathematics', pass_rate: 69.4, national_avg: 71.2 },
    { subject: 'Science', pass_rate: 74.8, national_avg: 73.1 },
  ];

  const infrastructureData = [
    { indicator: 'Schools with Electricity', value: 78, total: 142, percentage: 55 },
    { indicator: 'Schools with Internet', value: 45, total: 142, percentage: 32 },
    { indicator: 'Schools with Library', value: 89, total: 142, percentage: 63 },
    { indicator: 'Schools with Sanitation', value: 128, total: 142, percentage: 90 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Education Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Monitor education system performance and student outcomes
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          >
            <option value="all">All Levels</option>
            <option value="primary">Primary</option>
            <option value="secondary">Secondary</option>
            <option value="tvet">TVET</option>
          </select>
        </div>
      </div>

      {/* Overview Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Schools</p>
              <p className="text-2xl font-bold text-education-600">{overviewStats.schools}</p>
              <p className="text-sm text-gray-500">All levels</p>
            </div>
            <div className="p-3 bg-education-100 rounded-lg">
              <BuildingLibraryIcon className="h-6 w-6 text-education-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Students</p>
              <p className="text-2xl font-bold text-education-600">{overviewStats.students.toLocaleString()}</p>
              <p className="text-sm text-gray-500">Enrolled students</p>
            </div>
            <div className="p-3 bg-education-100 rounded-lg">
              <UsersIcon className="h-6 w-6 text-education-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Teachers</p>
              <p className="text-2xl font-bold text-education-600">{overviewStats.teachers.toLocaleString()}</p>
              <p className="text-sm text-gray-500">Active teachers</p>
            </div>
            <div className="p-3 bg-education-100 rounded-lg">
              <AcademicCapIcon className="h-6 w-6 text-education-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Primary Enrollment</p>
              <p className="text-2xl font-bold text-education-600">95.9%</p>
              <p className="text-sm text-gray-500">Net enrollment rate</p>
            </div>
            <div className="p-3 bg-education-100 rounded-lg">
              <ChartBarIcon className="h-6 w-6 text-education-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Enrollment by Education Level
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={enrollmentData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="level" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="enrolled" fill="#3B82F6" name="Enrolled" />
              <Bar dataKey="target" fill="#E5E7EB" name="Target" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Academic Performance by Subject
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="subject" angle={-45} textAnchor="end" height={80} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Bar dataKey="pass_rate" fill="#22c55e" name="District Pass Rate %" />
              <Bar dataKey="national_avg" fill="#f59e0b" name="National Average %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Infrastructure Status */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">School Infrastructure Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {infrastructureData.map((item, index) => (
            <div key={index} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-gray-900">{item.indicator}</h4>
                <span className="text-lg font-bold text-education-600">{item.percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div
                  className={`h-2 rounded-full ${
                    item.percentage >= 80 ? 'bg-green-500' :
                    item.percentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${item.percentage}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600">
                {item.value} out of {item.total} schools
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Education;