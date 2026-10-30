import React, { useEffect, useState } from 'react';
import { userService } from '../services/api';
import { toast } from 'react-toastify';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [completionPercentage, setCompletionPercentage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    loadProfile();
    loadCompletion();
  }, []);

  const loadProfile = async () => {
    try {
      const response = await userService.getProfile();
      setProfile(response.data);
      setFormData(response.data);
      setLoading(false);
    } catch (error) {
      toast.error('Failed to load profile');
      setLoading(false);
    }
  };

  const loadCompletion = async () => {
    try {
      const response = await userService.getProfileCompletion();
      setCompletionPercentage(response.data.completionPercentage);
    } catch (error) {
      console.log('Error loading completion');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await userService.updateProfile(formData);
      setProfile(formData);
      setEditing(false);
      toast.success('Profile updated successfully');
      loadCompletion();
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  const profileFields = [
    { label: 'Full Name', name: 'full_name', type: 'text' },
    { label: 'Email', name: 'email', type: 'email' },
    { label: 'Mobile', name: 'mobile_number', type: 'tel' },
    { label: 'Aadhaar', name: 'aadhaar_number', type: 'text' },
    { label: 'PAN', name: 'pan_number', type: 'text' },
    { label: 'Date of Birth', name: 'date_of_birth', type: 'date' },
    { label: 'Gender', name: 'gender', type: 'select', options: ['Male', 'Female', 'Other'] },
    { label: 'State', name: 'state', type: 'text' },
    { label: 'Occupation', name: 'occupation', type: 'text' },
    { label: 'Education', name: 'education', type: 'text' },
    { label: 'Annual Income', name: 'annual_income', type: 'number' },
    { label: 'Category', name: 'category', type: 'select', options: ['General', 'OBC', 'SC', 'ST'] }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      {/* Profile Completion */}
      <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
        <h2 className="text-2xl font-bold mb-4">Profile Completion</h2>
        <div className="flex items-center justify-between mb-4">
          <span className="text-lg font-semibold">{completionPercentage}% Complete</span>
          <span className="text-sm text-gray-600">Keep going! Complete your profile to get better recommendations.</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className="bg-gradient-to-r from-cyan-500 to-blue-500 h-4 rounded-full transition-all"
            style={{ width: `${completionPercentage}%` }}
          ></div>
        </div>
      </div>

      {/* Profile Form */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Your Profile</h2>
          <button
            onClick={() => setEditing(!editing)}
            className="px-4 py-2 bg-cyan-500 text-white rounded-lg hover:bg-cyan-600"
          >
            {editing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {editing ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {profileFields.map((field) => (
                <div key={field.name}>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">{field.label}</label>
                  {field.type === 'select' ? (
                    <select
                      name={field.name}
                      value={formData[field.name] || ''}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500"
                    >
                      <option value="">Select {field.label}</option>
                      {field.options.map(opt => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type={field.type}
                      name={field.name}
                      value={formData[field.name] || ''}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500"
                    />
                  )}
                </div>
              ))}
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 text-white py-3 rounded-lg font-bold hover:shadow-lg"
            >
              Save Changes
            </button>
          </form>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {profileFields.map((field) => (
              <div key={field.name} className="border-b pb-4">
                <p className="text-sm text-gray-600">{field.label}</p>
                <p className="font-semibold text-gray-900">{formData[field.name] || 'Not provided'}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
