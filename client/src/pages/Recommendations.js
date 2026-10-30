import React, { useEffect, useState } from 'react';
import { recommendationService, schemeService } from '../services/api';
import { toast } from 'react-toastify';
import { Star, MapPin, DollarSign, Calendar } from 'react-feather';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      const response = await recommendationService.getRecommendations();
      setRecommendations(response.data.recommendations);
      setLoading(false);
    } catch (error) {
      toast.error('Failed to load recommendations');
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold mb-2">Recommended Schemes For You</h1>
      <p className="text-gray-600 mb-8">Based on your profile, here are the best schemes matched for you.</p>

      {/* Filters */}
      <div className="flex space-x-4 mb-8 overflow-x-auto">
        {['all', 'Farmer', 'Student', 'Women', 'Disabled'].map(cat => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-6 py-2 rounded-full whitespace-nowrap font-semibold transition ${
              filter === cat
                ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Schemes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {recommendations.map((scheme, idx) => (
          <div
            key={idx}
            className="bg-white rounded-xl shadow-lg hover:shadow-2xl transition overflow-hidden"
          >
            {/* Card Header */}
            <div className="bg-gradient-to-r from-cyan-500 to-blue-500 p-6 text-white">
              <h3 className="text-xl font-bold mb-2">{scheme.scheme_name}</h3>
              <div className="flex items-center space-x-2">
                <Star size={20} className="text-yellow-300" />
                <span>{scheme.eligibility_score}% Eligible</span>
              </div>
            </div>

            {/* Card Body */}
            <div className="p-6 space-y-4">
              <p className="text-gray-600">{scheme.description}</p>

              {/* Benefits */}
              <div className="bg-cyan-50 p-4 rounded-lg">
                <h4 className="font-semibold mb-2 text-gray-900">Why You Qualify:</h4>
                <ul className="space-y-1 text-sm text-gray-700">
                  {scheme.explanation.map((reason, i) => (
                    <li key={i} className="flex items-center space-x-2">
                      <span className="w-2 h-2 bg-cyan-500 rounded-full"></span>
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-4 pt-4 border-t">
                <div className="text-center">
                  <DollarSign size={20} className="mx-auto text-cyan-500 mb-1" />
                  <p className="text-xs text-gray-600">Amount</p>
                </div>
                <div className="text-center">
                  <Calendar size={20} className="mx-auto text-cyan-500 mb-1" />
                  <p className="text-xs text-gray-600">Deadline</p>
                </div>
                <div className="text-center">
                  <MapPin size={20} className="mx-auto text-cyan-500 mb-1" />
                  <p className="text-xs text-gray-600">Available</p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="grid grid-cols-2 gap-4 pt-4">
                <button className="px-4 py-2 border-2 border-cyan-500 text-cyan-500 rounded-lg font-semibold hover:bg-cyan-50">
                  Learn More
                </button>
                <button className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg font-semibold hover:shadow-lg">
                  Apply Now
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;
