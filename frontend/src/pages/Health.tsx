import React, { useState } from 'react';
import {
  HeartIcon,
  UserGroupIcon,
  BuildingOffice2Icon,
  ExclamationTriangleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
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
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
} from 'recharts';

const Health: React.FC = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('monthly');
  const [selectedHealthFacility, setSelectedHealthFacility] = useState('all');

  // Mock data
  const overviewStats = {
    totalPatients: 12450,
    healthFacilities: 23,
    vaccinationRate: 89.5,
    maternalMortality: 2.1,
  };

  const diseaseData = [
    { name: 'Malaria', cases: 1250, trend: 15, severity: 'high' },
    { name: 'Respiratory Infections', cases: 890, trend: -8, severity: 'medium' },
    { name: 'Diarrheal Diseases', cases: 650, trend: -12, severity: 'low' },
    { name: 'Hypertension', cases: 420, trend: 5, severity: 'medium' },
    { name: 'Diabetes', cases: 180, trend: 12, severity: 'medium' },
  ];

  const monthlyTrends = [
    { month: 'Jan', malaria: 1100, respiratory: 950, diarrheal: 750 },
    { month: 'Feb', malaria: 1200, respiratory: 890, diarrheal: 680 },
    { month: 'Mar', malaria: 1350, respiratory: 820, diarrheal: 720 },
    { month: 'Apr', malaria: 1250, respiratory: 890, diarrheal: 650 },
    { month: 'May', malaria: 1180, respiratory: 940, diarrheal: 590 },
    { month: 'Jun', malaria: 1250, respiratory: 890, diarrheal: 650 },
  ];

  const vaccinationData = [
    { name: 'BCG', coverage: 92, target: 95 },
    { name: 'DPT', coverage: 88, target: 95 },
    { name: 'Polio', coverage: 94, target: 95 },
    { name: 'Measles', coverage: 87, target: 95 },
    { name: 'HPV', coverage: 76, target: 90 },
  ];

  const healthFacilities = [
    {
      name: 'Gasabo Health Center',
      type: 'Health Center',
      patients: 3240,
      capacity: 4000,
      staff: 45,
      equipment: 'Good',
    },
    {
      name: 'Kigali University Hospital',
      type: 'Hospital',
      patients: 5680,
      capacity: 6000,
      staff: 120,
      equipment: 'Excellent',
    },
    {
      name: 'Remera Health Post',
      type: 'Health Post',
      patients: 1850,
      capacity: 2000,
      staff: 15,
      equipment: 'Fair',
    },
  ];

  const challenges = [
    {
      issue: 'Malaria Outbreak',
      severity: 'high',
      affectedAreas: ['Kinyinya', 'Jabana'],
      cases: 1250,
      recommendation: 'Immediate deployment of bed nets and indoor spraying. Increase surveillance and community education programs.',
    },
    {
      issue: 'Vaccine Supply Shortage',
      severity: 'medium',
      affectedAreas: ['Remera', 'Kimironko'],
      cases: 0,
      recommendation: 'Emergency procurement of vaccines and temporary redistribution from other districts.',
    },
    {
      issue: 'Staff Shortage',
      severity: 'medium',
      affectedAreas: ['Multiple locations'],
      cases: 0,
      recommendation: 'Deploy mobile health teams and prioritize recruitment of critical care staff.',
    },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Health Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Monitor public health indicators and healthcare service delivery
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          >
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="quarterly">Quarterly</option>
            <option value="yearly">Yearly</option>
          </select>
          <select
            value={selectedHealthFacility}
            onChange={(e) => setSelectedHealthFacility(e.target.value)}
            className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          >
            <option value="all">All Facilities</option>
            <option value="hospital">Hospitals</option>
            <option value="health_center">Health Centers</option>
            <option value="health_post">Health Posts</option>
          </select>
        </div>
      </div>

      {/* Overview Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Patients"
          value={overviewStats.totalPatients.toLocaleString()}
          subtitle="This month"
          icon={UserGroupIcon}
          trend={3.2}
          trendDirection="up"
          color="health"
        />
        <StatCard
          title="Health Facilities"
          value={overviewStats.healthFacilities}
          subtitle="Active facilities"
          icon={BuildingOffice2Icon}
          trend={0}
          trendDirection="neutral"
          color="health"
        />
        <StatCard
          title="Vaccination Rate"
          value={`${overviewStats.vaccinationRate}%`}
          subtitle="Target: 95%"
          icon={HeartIcon}
          trend={2.1}
          trendDirection="up"
          color="health"
        />
        <StatCard
          title="Maternal Mortality"
          value={`${overviewStats.maternalMortality}%`}
          subtitle="Per 1000 births"
          icon={ExclamationTriangleIcon}
          trend={-0.3}
          trendDirection="down"
          color="health"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Disease Trends */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Disease Trends (Monthly)
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={monthlyTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="malaria" stroke="#ef4444" strokeWidth={2} />
              <Line type="monotone" dataKey="respiratory" stroke="#f59e0b" strokeWidth={2} />
              <Line type="monotone" dataKey="diarrheal" stroke="#22c55e" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Vaccination Coverage */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Vaccination Coverage vs Targets
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={vaccinationData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="coverage" fill="#22c55e" name="Current Coverage" />
              <Bar dataKey="target" fill="#e5e7eb" name="Target" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Current Disease Cases */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Current Disease Cases & Trends</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Disease
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Current Cases
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Trend
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Severity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Action Required
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {diseaseData.map((disease, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {disease.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {disease.cases.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      {disease.trend > 0 ? (
                        <ArrowTrendingUpIcon className="h-4 w-4 text-red-500 mr-1" />
                      ) : (
                        <ArrowTrendingDownIcon className="h-4 w-4 text-green-500 mr-1" />
                      )}
                      <span className={`text-sm ${disease.trend > 0 ? 'text-red-600' : 'text-green-600'}`}>
                        {Math.abs(disease.trend)}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        disease.severity === 'high'
                          ? 'bg-red-100 text-red-800'
                          : disease.severity === 'medium'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-green-100 text-green-800'
                      }`}
                    >
                      {disease.severity.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {disease.severity === 'high' ? 'Immediate' : disease.severity === 'medium' ? 'Monitor' : 'Routine'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Health Facilities */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Health Facilities Overview</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {healthFacilities.map((facility, index) => (
              <div key={index} className="border rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-2">{facility.name}</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Type:</span>
                    <span className="font-medium">{facility.type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Patients:</span>
                    <span className="font-medium">{facility.patients.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Capacity:</span>
                    <span className="font-medium">
                      {Math.round((facility.patients / facility.capacity) * 100)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Staff:</span>
                    <span className="font-medium">{facility.staff}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Equipment:</span>
                    <span
                      className={`font-medium ${
                        facility.equipment === 'Excellent'
                          ? 'text-green-600'
                          : facility.equipment === 'Good'
                          ? 'text-blue-600'
                          : 'text-yellow-600'
                      }`}
                    >
                      {facility.equipment}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Health Challenges & AI Recommendations */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Health Challenges & AI Recommendations
          </h3>
        </div>
        <div className="p-6 space-y-4">
          {challenges.map((challenge, index) => (
            <div key={index} className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-gray-900">{challenge.issue}</h4>
                <span
                  className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    challenge.severity === 'high'
                      ? 'bg-red-100 text-red-800'
                      : challenge.severity === 'medium'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-green-100 text-green-800'
                  }`}
                >
                  {challenge.severity.toUpperCase()}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">
                Affected Areas: {challenge.affectedAreas.join(', ')}
                {challenge.cases > 0 && ` • Cases: ${challenge.cases.toLocaleString()}`}
              </p>
              <div className="bg-blue-50 p-3 rounded">
                <p className="text-sm font-medium text-blue-800">AI Recommendation:</p>
                <p className="text-sm text-blue-700">{challenge.recommendation}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Stat Card Component
const StatCard: React.FC<{
  title: string;
  value: string | number;
  subtitle: string;
  icon: React.ComponentType<any>;
  trend: number;
  trendDirection: 'up' | 'down' | 'neutral';
  color: string;
}> = ({ title, value, subtitle, icon: Icon, trend, trendDirection, color }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-red-600">{value}</p>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        </div>
        <div className="p-3 bg-red-100 rounded-lg">
          <Icon className="h-6 w-6 text-red-600" />
        </div>
      </div>
      {trend !== 0 && (
        <div className="mt-4 flex items-center">
          {trendDirection === 'up' ? (
            <ArrowTrendingUpIcon className="h-4 w-4 text-green-500 mr-1" />
          ) : trendDirection === 'down' ? (
            <ArrowTrendingDownIcon className="h-4 w-4 text-red-500 mr-1" />
          ) : null}
          <span className={`text-sm ${
            trendDirection === 'up' ? 'text-green-600' : 
            trendDirection === 'down' ? 'text-red-600' : 
            'text-gray-600'
          }`}>
            {Math.abs(trend)}% vs last month
          </span>
        </div>
      )}
    </div>
  );
};

export default Health;