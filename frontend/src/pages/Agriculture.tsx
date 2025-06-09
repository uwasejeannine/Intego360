import React, { useState } from 'react';
import {
  UsersIcon,
  MapPinIcon,
  ArrowTrendingUpIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
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
  AreaChart,
  Area,
} from 'recharts';

const Agriculture: React.FC = () => {
  const [selectedSeason, setSelectedSeason] = useState('2025-A');
  const [selectedCrop, setSelectedCrop] = useState('all');

  // Mock data
  const overviewStats = {
    totalFarmers: 45620,
    cultivatedLand: 28450,
    seasonalProduction: 125400,
    cooperatives: 156,
  };

  const cropsData = [
    { name: 'Maize', production: 45200, target: 48000, yield: 2.8, area: 16142 },
    { name: 'Beans', production: 32100, target: 35000, yield: 1.9, area: 16894 },
    { name: 'Cassava', production: 28800, target: 30000, yield: 12.5, area: 2304 },
    { name: 'Sweet Potato', production: 19500, target: 22000, yield: 8.9, area: 2191 },
    { name: 'Rice', production: 15200, target: 18000, yield: 4.2, area: 3619 },
  ];

  const seasonalTrends = [
    { month: 'Sep', seasonA: 32, seasonB: 0, seasonC: 15 },
    { month: 'Oct', seasonA: 45, seasonB: 0, seasonC: 28 },
    { month: 'Nov', seasonA: 68, seasonB: 0, seasonC: 12 },
    { month: 'Dec', seasonA: 85, seasonB: 0, seasonC: 5 },
    { month: 'Jan', seasonA: 92, seasonB: 0, seasonC: 0 },
    { month: 'Feb', seasonA: 78, seasonB: 12, seasonC: 0 },
  ];

  const challenges = [
    {
      issue: 'Climate Change Impact',
      severity: 'high',
      affectedFarmers: 12450,
      locations: ['Kinyinya', 'Jabana'],
      recommendation: 'Deploy drought-resistant seed varieties and establish irrigation systems in affected areas. Coordinate with meteorology services for early warning systems.',
    },
    {
      issue: 'Seed Quality',
      severity: 'medium',
      affectedFarmers: 8200,
      locations: ['Remera', 'Gisozi'],
      recommendation: 'Strengthen quality control measures and establish certified seed distribution centers. Partner with agricultural research institutes.',
    },
    {
      issue: 'Market Access',
      severity: 'medium',
      affectedFarmers: 6800,
      locations: ['Kimironko'],
      recommendation: 'Develop market linkage programs and improve rural road infrastructure. Establish collection centers and negotiate with buyers.',
    },
  ];

  const cooperatives = [
    {
      name: 'COOPAGRI Kinyinya',
      members: 245,
      crops: ['Maize', 'Beans'],
      performance: 87,
      revenue: 2450000,
    },
    {
      name: 'COOPAGRI Remera',
      members: 189,
      crops: ['Rice', 'Vegetables'],
      performance: 92,
      revenue: 3200000,
    },
    {
      name: 'COOPAGRI Kimironko',
      members: 156,
      crops: ['Cassava', 'Sweet Potato'],
      performance: 78,
      revenue: 1800000,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Agriculture Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Monitor agricultural performance and support farmer development
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <select
            value={selectedSeason}
            onChange={(e) => setSelectedSeason(e.target.value)}
            className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          >
            <option value="2025-A">Season A 2025</option>
            <option value="2024-C">Season C 2024</option>
            <option value="2024-B">Season B 2024</option>
          </select>
          <select
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          >
            <option value="all">All Crops</option>
            <option value="maize">Maize</option>
            <option value="beans">Beans</option>
            <option value="cassava">Cassava</option>
            <option value="rice">Rice</option>
          </select>
        </div>
      </div>

      {/* Overview Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Farmers"
          value={overviewStats.totalFarmers.toLocaleString()}
          subtitle="Registered farmers"
          icon={UsersIcon}
          trend={3.2}
          color="agriculture"
        />
        <StatCard
          title="Cultivated Land"
          value={`${overviewStats.cultivatedLand.toLocaleString()} Ha`}
          subtitle="Total hectares"
          icon={MapPinIcon}
          trend={1.8}
          color="agriculture"
        />
        <StatCard
          title="Seasonal Production"
          value={`${overviewStats.seasonalProduction.toLocaleString()} MT`}
          subtitle="Metric tons"
          icon={ArrowTrendingUpIcon}
          trend={8.5}
          color="agriculture"
        />
        <StatCard
          title="Cooperatives"
          value={overviewStats.cooperatives}
          subtitle="Active cooperatives"
          icon={ChartBarIcon}
          trend={2.1}
          color="agriculture"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Crop Production vs Targets */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Crop Production vs Targets
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cropsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="production" fill="#22c55e" name="Actual Production" />
              <Bar dataKey="target" fill="#e5e7eb" name="Target" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Seasonal Activity Calendar */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Seasonal Activity Calendar
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={seasonalTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="seasonA"
                stackId="1"
                stroke="#22c55e"
                fill="#22c55e"
                fillOpacity={0.6}
              />
              <Area
                type="monotone"
                dataKey="seasonB"
                stackId="1"
                stroke="#f59e0b"
                fill="#f59e0b"
                fillOpacity={0.6}
              />
              <Area
                type="monotone"
                dataKey="seasonC"
                stackId="1"
                stroke="#ef4444"
                fill="#ef4444"
                fillOpacity={0.6}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Crop Performance */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Detailed Crop Performance</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Crop
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Production (MT)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Target (MT)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Achievement
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Yield (T/Ha)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Area (Ha)
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {cropsData.map((crop, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {crop.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {crop.production.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {crop.target.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        crop.production / crop.target >= 0.9
                          ? 'bg-green-100 text-green-800'
                          : crop.production / crop.target >= 0.7
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {Math.round((crop.production / crop.target) * 100)}%
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {crop.yield}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {crop.area.toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Challenges & AI Recommendations */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Current Challenges & AI Recommendations
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
                Affecting {challenge.affectedFarmers.toLocaleString()} farmers in{' '}
                {challenge.locations.join(', ')}
              </p>
              <div className="bg-blue-50 p-3 rounded">
                <p className="text-sm font-medium text-blue-800">AI Recommendation:</p>
                <p className="text-sm text-blue-700">{challenge.recommendation}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cooperatives Performance */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Top Performing Cooperatives</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {cooperatives.map((coop, index) => (
              <div key={index} className="border rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-2">{coop.name}</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Members:</span>
                    <span className="font-medium">{coop.members}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Crops:</span>
                    <span className="font-medium">{coop.crops.join(', ')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Performance:</span>
                    <span
                      className={`font-medium ${
                        coop.performance >= 85
                          ? 'text-green-600'
                          : coop.performance >= 70
                          ? 'text-yellow-600'
                          : 'text-red-600'
                      }`}
                    >
                      {coop.performance}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Revenue:</span>
                    <span className="font-medium">
                      {(coop.revenue / 1000000).toFixed(1)}M RWF
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
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
  color: string;
}> = ({ title, value, subtitle, icon: Icon, trend, color }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-green-600">{value}</p>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        </div>
        <div className="p-3 bg-green-100 rounded-lg">
          <Icon className="h-6 w-6 text-green-600" />
        </div>
      </div>
      {trend && (
        <div className="mt-4 flex items-center">
          <ArrowTrendingUpIcon className="h-4 w-4 text-green-500 mr-1" />
          <span className="text-sm text-green-600">{Math.abs(trend)}% vs last month</span>
        </div>
      )}
    </div>
  );
};

export default Agriculture;