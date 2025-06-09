// Reports.tsx
import React from 'react';

const Reports: React.FC = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Reports & Analytics</h1>
      <div className="bg-white rounded-lg p-8 shadow-sm border text-center">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Reports Module</h3>
        <p className="text-gray-600 mb-6">
          This section will provide comprehensive reporting capabilities including automated report generation, 
          data export, and advanced analytics visualizations.
        </p>
        <button className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
          Coming Soon
        </button>
      </div>
    </div>
  );
};

export default Reports;
