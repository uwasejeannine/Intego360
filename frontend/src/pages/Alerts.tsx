import React from 'react';
import { ExclamationTriangleIcon, BellIcon } from '@heroicons/react/24/outline';

const Alerts: React.FC = () => {
  const alerts = [
    { id: 1, type: 'critical', sector: 'Health', message: 'Malaria cases increased by 15% in Kinyinya sector', time: '2 hours ago', priority: 'high' },
    { id: 2, type: 'warning', sector: 'Agriculture', message: 'Drought conditions affecting 3 sectors', time: '4 hours ago', priority: 'medium' },
    { id: 3, type: 'info', sector: 'Education', message: 'New school construction completed in Remera', time: '1 day ago', priority: 'low' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">System Alerts & Notifications</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-red-50 rounded-lg p-4 border border-red-200">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-8 w-8 text-red-600 mr-3" />
            <div>
              <p className="text-2xl font-bold text-red-600">
                {alerts.filter(a => a.priority === 'high').length}
              </p>
              <p className="text-sm text-red-800">Critical Alerts</p>
            </div>
          </div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-8 w-8 text-yellow-600 mr-3" />
            <div>
              <p className="text-2xl font-bold text-yellow-600">
                {alerts.filter(a => a.priority === 'medium').length}
              </p>
              <p className="text-sm text-yellow-800">Medium Alerts</p>
            </div>
          </div>
        </div>
        <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <div className="flex items-center">
            <BellIcon className="h-8 w-8 text-blue-600 mr-3" />
            <div>
              <p className="text-2xl font-bold text-blue-600">
                {alerts.filter(a => a.priority === 'low').length}
              </p>
              <p className="text-sm text-blue-800">Info Alerts</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Alerts</h3>
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div key={alert.id} className={`border rounded-lg p-4 ${
              alert.priority === 'high' ? 'border-red-200 bg-red-50' :
              alert.priority === 'medium' ? 'border-yellow-200 bg-yellow-50' :
              'border-blue-200 bg-blue-50'
            }`}>
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <ExclamationTriangleIcon className={`h-5 w-5 mt-0.5 ${
                    alert.priority === 'high' ? 'text-red-500' :
                    alert.priority === 'medium' ? 'text-yellow-500' :
                    'text-blue-500'
                  }`} />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        alert.priority === 'high' ? 'bg-red-100 text-red-800' :
                        alert.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {alert.priority.toUpperCase()}
                      </span>
                      <span className="text-sm font-medium text-gray-600">{alert.sector}</span>
                      <span className="text-xs text-gray-500">{alert.time}</span>
                    </div>
                    <p className="text-sm font-medium text-gray-900 mb-2">{alert.message}</p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button className="px-3 py-1 text-xs font-medium text-blue-600 bg-blue-100 rounded hover:bg-blue-200">
                    View Details
                  </button>
                  <button className="px-3 py-1 text-xs font-medium text-green-600 bg-green-100 rounded hover:bg-green-200">
                    Mark Resolved
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Alerts;