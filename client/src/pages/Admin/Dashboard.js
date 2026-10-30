import React, { useEffect, useState } from 'react';
import { adminService } from '../../services/api';
import { toast } from 'react-toastify';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('stats');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await adminService.getStats();
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      toast.error('Failed to load admin stats');
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  const lineChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [
      {
        label: 'Users',
        data: [400, 500, 600, 750],
        borderColor: '#0ea5e9',
        backgroundColor: 'rgba(14, 165, 233, 0.2)',
        tension: 0.3
      }
    ]
  };

  const barChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [
      {
        label: 'Applications',
        data: [240, 300, 400, 450],
        backgroundColor: '#3b82f6'
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-8">Admin Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <p className="text-gray-600 text-sm mb-2">Total Users</p>
          <p className="text-4xl font-bold text-cyan-500">{stats?.totalUsers}</p>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <p className="text-gray-600 text-sm mb-2">Active Users</p>
          <p className="text-4xl font-bold text-blue-500">{stats?.activeUsers}</p>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <p className="text-gray-600 text-sm mb-2">Total Schemes</p>
          <p className="text-4xl font-bold text-green-500">{stats?.totalSchemes}</p>
        </div>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <p className="text-gray-600 text-sm mb-2">User Growth</p>
          <p className="text-4xl font-bold text-purple-500">{stats?.userGrowth}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-4 mb-8 bg-white rounded-lg shadow-lg p-4">
        {['stats', 'users', 'schemes', 'model'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-2 rounded-lg font-semibold transition capitalize ${
              activeTab === tab
                ? 'bg-cyan-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      {activeTab === 'stats' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4">User Growth</h2>
            <div className="h-64">
              <Line data={lineChartData} options={chartOptions} />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4">Applications</h2>
            <div className="h-64">
              <Bar data={barChartData} options={chartOptions} />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">User Management</h2>
          <p className="text-gray-600">User management interface coming soon...</p>
        </div>
      )}

      {activeTab === 'schemes' && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Scheme Management</h2>
          <p className="text-gray-600">Scheme management interface coming soon...</p>
        </div>
      )}

      {activeTab === 'model' && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4">ML Model Management</h2>
          <button className="px-6 py-3 bg-cyan-500 text-white rounded-lg font-bold hover:bg-cyan-600">
            Retrain Model
          </button>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
