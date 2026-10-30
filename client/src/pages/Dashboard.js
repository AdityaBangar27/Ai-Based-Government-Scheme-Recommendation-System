import React from 'react';

const Dashboard = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Welcome Back!</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {/* Stats Cards */}
        {[
          { title: 'Profile Completion', value: '85%', icon: '📊' },
          { title: 'Eligible Schemes', value: '12', icon: '✅' },
          { title: 'Applications', value: '3', icon: '📝' },
          { title: 'Active Benefits', value: '2', icon: '💰' }
        ].map((stat, idx) => (
          <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
            <div className="text-3xl mb-2">{stat.icon}</div>
            <p className="text-gray-600 text-sm">{stat.title}</p>
            <p className="text-3xl font-bold text-cyan-500">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Recommendations */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Recommendations</h2>
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="flex items-center justify-between p-4 bg-cyan-50 rounded-lg hover:bg-cyan-100 cursor-pointer">
                <div>
                  <p className="font-semibold">Scheme Name {i}</p>
                  <p className="text-sm text-gray-600">85% Eligible • Applied 2 days ago</p>
                </div>
                <button className="px-4 py-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600">
                  View
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <button className="w-full px-4 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg font-semibold hover:shadow-lg">
              Complete Profile
            </button>
            <button className="w-full px-4 py-3 bg-gray-200 text-gray-900 rounded-lg font-semibold hover:bg-gray-300">
              Upload Documents
            </button>
            <button className="w-full px-4 py-3 bg-gray-200 text-gray-900 rounded-lg font-semibold hover:bg-gray-300">
              Track Applications
            </button>
            <button className="w-full px-4 py-3 bg-gray-200 text-gray-900 rounded-lg font-semibold hover:bg-gray-300">
              Browse Schemes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
