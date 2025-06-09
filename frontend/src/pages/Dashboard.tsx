import React, { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../hooks/useAuth';
import { authAPI } from '../api/auth';
import {
  UsersIcon,
  ChartBarIcon,
  HeartIcon,
  AcademicCapIcon,
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
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

const Dashboard: React.FC = () => {
  const { user } = useAuth() as { user: any } ;

  // Log dashboard view
  useEffect(() => {
    authAPI.logDashboardView().catch(console.error);
  }, []);

  // Fetch dashboard data
  const { data: dashboardData, isLoading } = useQuery({
    queryKey: ['dashboard-overview'],
    queryFn: () => authAPI.getDashboardOverview(),
  });

  const { data: recentActivities } = useQuery({
    queryKey: ['recent-activities'],
    queryFn: () => authAPI.getRecentActivities(),
  });

  // Mock data for demonstration
  const sectorsData = [
    { name: 'Kinyinya', agriculture: 78, health: 85, education: 92 },
    { name: 'Remera', agriculture: 82, health: 88, education: 89 },
    { name: 'Kimironko', agriculture: 75, health: 91, education: 87 },
    { name: 'Gisozi', agriculture: 88, health: 83, education: 94 },
    { name: 'Jabana', agriculture: 71, health: 86, education: 88 },
    { name: 'Jali', agriculture: 84, health: 89, education: 91 },
  ];

  const agricultureTrends = [
    { month: 'Sep', seasonA: 32, seasonB: 0, seasonC: 15 },
    { month: 'Oct', seasonA: 45, seasonB: 0, seasonC: 28 },
    { month: 'Nov', seasonA: 68, seasonB: 0, seasonC: 12 },
    { month: 'Dec', seasonA: 85, seasonB: 0, seasonC: 5 },
    { month: 'Jan', seasonA: 92, seasonB: 0, seasonC: 0 },
    { month: 'Feb', seasonA: 78, seasonB: 12, seasonC: 0 },
  ];

  const performanceData = [
    { name: 'Agriculture', value: 78, color: '#22c55e' },
    { name: 'Health', value: 87, color: '#ef4444' },
    { name: 'Education', value: 91, color: '#3b82f6' },
  ];

  const alerts = [
    {
      id: 1,
      type: 'critical',
      sector: 'Health',
      message: 'Malaria cases increased by 15% in Kinyinya sector',
      time: '2 hours ago',
      priority: 'high',
    },
    {
      id: 2,
      type: 'warning',
      sector: 'Agriculture',
      message: 'Drought conditions affecting 3 sectors',
      time: '4 hours ago',
      priority: 'medium',
    },
    {
      id: 3,
      type: 'info',
      sector: 'Education',
      message: 'New school construction completed in Remera',
      time: '1 day ago',
      priority: 'low',
    },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-[#137775] rounded-lg shadow-lg p-6 text-white">
        <h1 className="text-2xl font-bold">
          Welcome back, {user?.full_name || 'User'}!
        </h1>
        <p className="text-primary-100 mt-2">
          {user?.district ? `Managing ${user.district} District` : 'System Administrator'}
        </p>
        <div className="mt-4 flex items-center space-x-4">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-400 rounded-full mr-2"></div>
            <span className="text-sm">System Status: Operational</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-yellow-400 rounded-full mr-2"></div>
            <span className="text-sm">3 Active Alerts</span>
          </div>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Population"
          value="486,240"
          subtitle={user?.district ? `${user.district} District` : 'All Districts'}
          icon={UsersIcon}
          trend={{ value: 2.3, direction: 'up' }}
          color="blue"
        />
        <MetricCard
          title="Active Farmers"
          value="45,620"
          subtitle="Registered in system"
          icon={ChartBarIcon}
          trend={{ value: 5.2, direction: 'up' }}
          color="green"
        />
        <MetricCard
          title="Health Facilities"
          value="48"
          subtitle="All levels"
          icon={HeartIcon}
          trend={{ value: 0, direction: 'stable' }}
          color="red"
        />
        <MetricCard
          title="Schools"
          value="142"
          subtitle="All levels"
          icon={AcademicCapIcon}
          trend={{ value: 1.4, direction: 'up' }}
          color="purple"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sector Performance Overview */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Sector Performance Overview
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sectorsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="agriculture" fill="#22c55e" name="Agriculture" />
              <Bar dataKey="health" fill="#ef4444" name="Health" />
              <Bar dataKey="education" fill="#3b82f6" name="Education" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Performance Distribution */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Overall Performance Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={performanceData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {performanceData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Agricultural Seasonal Trends */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Agricultural Seasonal Trends
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={agricultureTrends}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="seasonA"
              stroke="#22c55e"
              name="Season A"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="seasonB"
              stroke="#f59e0b"
              name="Season B"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="seasonC"
              stroke="#ef4444"
              name="Season C"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Alerts and Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Alerts */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Recent Alerts</h3>
            <ExclamationTriangleIcon className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`flex items-start space-x-3 p-3 rounded-lg ${
                  alert.priority === 'high'
                    ? 'bg-red-50 border border-red-200'
                    : alert.priority === 'medium'
                    ? 'bg-yellow-50 border border-yellow-200'
                    : 'bg-blue-50 border border-blue-200'
                }`}
              >
                <ExclamationTriangleIcon
                  className={`h-5 w-5 mt-0.5 ${
                    alert.priority === 'high'
                      ? 'text-red-500'
                      : alert.priority === 'medium'
                      ? 'text-yellow-500'
                      : 'text-blue-500'
                  }`}
                />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                  <p className="text-xs text-gray-500">
                    {alert.sector} • {alert.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4">
            <button className="w-full text-center text-sm text-primary-600 hover:text-primary-500 font-medium">
              View all alerts →
            </button>
          </div>
        </div>

        {/* Recent Activities */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activities</h3>
          <div className="space-y-3">
            {recentActivities?.data?.slice(0, 5).map((activity: any, index: number) => (
              <div key={index} className="flex items-start space-x-3">
                <div className="w-2 h-2 bg-primary-600 rounded-full mt-2"></div>
                <div className="flex-1">
                  <p className="text-sm text-gray-900">{activity.description}</p>
                  <p className="text-xs text-gray-500">
                    {new Date(activity.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            )) || (
              <div className="text-center text-gray-500 py-4">
                <p className="text-sm">No recent activities</p>
              </div>
            )}
          </div>
          <div className="mt-4">
            <button className="w-full text-center text-sm text-primary-600 hover:text-primary-500 font-medium">
              View all activities →
            </button>
          </div>
        </div>
      </div>

    </div>
  );
};

// Metric Card Component
const MetricCard: React.FC<{
  title: string;
  value: string;
  subtitle: string;
  icon: React.ComponentType<any>;
  trend: { value: number; direction: 'up' | 'down' | 'stable' };
  color: string;
}> = ({ title, value, subtitle, icon: Icon, trend, color }) => {
  const colorClasses = {
    blue: 'text- bg-[#137775] bg-blue-100',
    green: 'text-green-600 bg-green-100',
    red: 'text-red-600 bg-red-100',
    purple: 'text-purple-600 bg-purple-100',
    yellow: 'text-yellow-600 bg-yellow-100',
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color as keyof typeof colorClasses]}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
      {trend && (
        <div className="mt-4 flex items-center">
          {trend.direction === 'up' ? (
            <ArrowTrendingUpIcon className="h-4 w-4 text-green-500 mr-1" />
          ) : trend.direction === 'down' ? (
            <ArrowTrendingDownIcon className="h-4 w-4 text-red-500 mr-1" />
          ) : (
            <div className="h-4 w-4 bg-gray-400 rounded-full mr-1"></div>
          )}
          <span
            className={`text-sm ${
              trend.direction === 'up'
                ? 'text-green-600'
                : trend.direction === 'down'
                ? 'text-red-600'
                : 'text-gray-600'
            }`}
          >
            {trend.direction === 'stable' ? 'No change' : `${trend.value}% vs last month`}
          </span>
        </div>
      )}
    </div>
  );
};

// Quick Action Button Component
const QuickActionButton: React.FC<{
  icon: React.ComponentType<any>;
  label: string;
  href: string;
  color: string;
}> = ({ icon: Icon, label, href, color }) => {
  const colorClasses = {
    green: 'text-green-600 bg-green-50 hover:bg-green-100 border-green-200',
    red: 'text-red-600 bg-red-50 hover:bg-red-100 border-red-200',
    blue: 'text-blue-600 bg-blue-50 hover:bg-blue-100 border-blue-200',
    yellow: 'text-yellow-600 bg-yellow-50 hover:bg-yellow-100 border-yellow-200',
  };

  return (
    <a
      href={href}
      className={`flex flex-col items-center p-4 rounded-lg border transition-colors duration-200 ${
        colorClasses[color as keyof typeof colorClasses]
      }`}
    >
      <Icon className="h-8 w-8 mb-2" />
      <span className="text-sm font-medium text-center">{label}</span>
    </a>
  );
};

export default Dashboard;