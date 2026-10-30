import React, { useState } from 'react';
import { recommendationService } from '../services/api';
import { toast } from 'react-toastify';
import {
  Search,
  CheckCircle,
  ExternalLink,
  Award,
  FileText,
  User,
  DollarSign,
  Briefcase,
  AlertCircle,
  RotateCcw,
  Zap,
  ChevronRight
} from 'react-feather';

const PRESETS = [
  {
    name: '🌾 Small Farmer',
    data: {
      age: 36,
      income: 85000,
      gender: 'Male',
      occupation: 'Farmer',
      education: '10th Pass',
      category: 'OBC',
      state: 'Maharashtra',
      disability_status: 'No',
      farmer_status: 'Yes',
      student_status: 'No',
      employment_status: 'Self-Employed'
    }
  },
  {
    name: '🎓 College Student',
    data: {
      age: 20,
      income: 45000,
      gender: 'Female',
      occupation: 'Student',
      education: '12th Pass',
      category: 'General',
      state: 'Delhi',
      disability_status: 'No',
      farmer_status: 'No',
      student_status: 'Yes',
      employment_status: 'Unemployed'
    }
  },
  {
    name: '🛠️ Rural Artisan',
    data: {
      age: 32,
      income: 110000,
      gender: 'Male',
      occupation: 'Artisan',
      education: '10th Pass',
      category: 'SC',
      state: 'Uttar Pradesh',
      disability_status: 'No',
      farmer_status: 'No',
      student_status: 'No',
      employment_status: 'Self-Employed'
    }
  },
  {
    name: '💼 Unorganized Worker',
    data: {
      age: 35,
      income: 140000,
      gender: 'Male',
      occupation: 'Unorganized worker',
      education: '10th Pass',
      category: 'General',
      state: 'All States',
      disability_status: 'No',
      farmer_status: 'No',
      student_status: 'No',
      employment_status: 'Employed'
    }
  }
];

const STATES = [
  'All States',
  'Andhra Pradesh',
  'Bihar',
  'Delhi',
  'Gujarat',
  'Haryana',
  'Karnataka',
  'Kerala',
  'Madhya Pradesh',
  'Maharashtra',
  'Punjab',
  'Rajasthan',
  'Tamil Nadu',
  'Telangana',
  'Uttar Pradesh',
  'West Bengal'
];

const OCCUPATIONS = [
  'Farmer',
  'Student',
  'Artisan',
  'Unorganized worker',
  'Salaried Employee',
  'Self-Employed',
  'Unemployed',
  'Business / Trader',
  'Daily Wage Labourer',
  'Homemaker'
];

const Home = () => {
  const [formData, setFormData] = useState({
    age: 28,
    income: 120000,
    gender: 'Male',
    occupation: 'Farmer',
    education: 'Graduate',
    category: 'General',
    state: 'Maharashtra',
    disability_status: 'No',
    farmer_status: 'Yes',
    student_status: 'No',
    employment_status: 'Employed'
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [activeFilter, setActiveFilter] = useState('all');
  const [selectedScheme, setSelectedScheme] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const applyPreset = (preset) => {
    setFormData(preset.data);
    fetchRecommendations(preset.data);
  };

  const resetForm = () => {
    setFormData({
      age: 25,
      income: 100000,
      gender: 'Male',
      occupation: 'General',
      education: 'Graduate',
      category: 'General',
      state: 'All States',
      disability_status: 'No',
      farmer_status: 'No',
      student_status: 'No',
      employment_status: 'Employed'
    });
    setResults(null);
  };

  const fetchRecommendations = async (dataToSubmit = formData) => {
    setLoading(true);
    try {
      const response = await recommendationService.getRecommendations(dataToSubmit);
      setResults(response.data);
      toast.success(
        `Found ${response.data.eligibleCount || response.data.recommendations?.length || 0} eligible schemes!`
      );
      // Smooth scroll to results
      setTimeout(() => {
        const el = document.getElementById('results-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 150);
    } catch (error) {
      toast.error('Failed to generate recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchRecommendations();
  };

  // Filter schemes
  const getFilteredSchemes = () => {
    if (!results || !results.recommendations) return [];
    if (activeFilter === 'eligible') {
      return results.recommendations.filter((s) => s.isEligible);
    }
    if (activeFilter === 'high') {
      return results.recommendations.filter((s) => (s.recommendationScore || 0) >= 80);
    }
    if (activeFilter === 'farmer') {
      return results.recommendations.filter(
        (s) => s.category?.toLowerCase().includes('farmer') || s.scheme_name?.toLowerCase().includes('kisan')
      );
    }
    if (activeFilter === 'student') {
      return results.recommendations.filter(
        (s) => s.category?.toLowerCase().includes('student') || s.scheme_name?.toLowerCase().includes('scholarship')
      );
    }
    return results.recommendations;
  };

  const filteredSchemes = getFilteredSchemes();

  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header Hero */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-cyan-100 text-cyan-800 rounded-full text-xs font-semibold uppercase tracking-wider mb-3">
            <Zap size={14} className="text-cyan-600" />
            <span>AI Random Forest Recommendation Engine</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
            Government Scheme Eligibility & Recommendation
          </h1>
          <p className="mt-2 text-base sm:text-lg text-gray-600 max-w-2xl mx-auto">
            Enter your demographic and financial details below to discover all central & state schemes you are eligible for.
          </p>
        </div>

        {/* Quick Demo Profile Presets */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
              ⚡ Quick Fill Test Profiles:
            </div>
            <div className="flex flex-wrap gap-2 w-full sm:w-auto">
              {PRESETS.map((preset, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => applyPreset(preset)}
                  className="px-3 py-1.5 bg-gray-100 hover:bg-cyan-50 hover:text-cyan-700 hover:border-cyan-300 border border-gray-200 rounded-lg text-xs font-medium text-gray-700 transition"
                >
                  {preset.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main Eligibility Form Card */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 sm:p-8 mb-10">
          <div className="flex items-center justify-between border-b border-gray-100 pb-4 mb-6">
            <div className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-lg bg-cyan-500 text-white flex items-center justify-center font-bold">
                <FileText size={20} />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Eligibility Form</h2>
                <p className="text-xs text-gray-500">Provide details for accurate ML evaluation</p>
              </div>
            </div>
            <button
              type="button"
              onClick={resetForm}
              className="inline-flex items-center space-x-1 text-xs text-gray-500 hover:text-gray-800 transition"
            >
              <RotateCcw size={14} />
              <span>Reset</span>
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Section 1: Demographics */}
            <div>
              <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                <User size={15} className="text-cyan-500" />
                <span>1. Personal & Demographic Details</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Age */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Age (Years) <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="age"
                    min="1"
                    max="100"
                    value={formData.age}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                    required
                  />
                </div>

                {/* Gender */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Gender <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                    <option value="All">All / Prefer not to say</option>
                  </select>
                </div>

                {/* Social Category */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Social Category <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                  >
                    <option value="General">General</option>
                    <option value="OBC">OBC (Other Backward Class)</option>
                    <option value="SC">SC (Scheduled Caste)</option>
                    <option value="ST">ST (Scheduled Tribe)</option>
                    <option value="EWS">EWS (Economically Weaker Section)</option>
                  </select>
                </div>

                {/* State / UT */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    State / UT <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="state"
                    value={formData.state}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                  >
                    {STATES.map((s, idx) => (
                      <option key={idx} value={s}>
                        {s}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Section 2: Financial & Employment */}
            <div className="pt-2">
              <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                <DollarSign size={15} className="text-cyan-500" />
                <span>2. Income & Education Profile</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Annual Income */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Annual Family Income (₹) <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-500 text-sm">
                      ₹
                    </span>
                    <input
                      type="number"
                      name="income"
                      min="0"
                      step="5000"
                      value={formData.income}
                      onChange={handleChange}
                      placeholder="e.g. 150000"
                      className="w-full pl-7 pr-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                      required
                    />
                  </div>
                </div>

                {/* Occupation */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Occupation <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="occupation"
                    value={formData.occupation}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                  >
                    {OCCUPATIONS.map((occ, idx) => (
                      <option key={idx} value={occ}>
                        {occ}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Education */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Education Level <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="education"
                    value={formData.education}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                  >
                    <option value="Illiterate">Below 10th / Illiterate</option>
                    <option value="10th Pass">10th Pass</option>
                    <option value="12th Pass">12th Pass</option>
                    <option value="Graduate">Graduate</option>
                    <option value="Post Graduate">Post Graduate / Professional</option>
                  </select>
                </div>

                {/* Employment Status */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Employment Status <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="employment_status"
                    value={formData.employment_status}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
                  >
                    <option value="Employed">Employed (Salaried)</option>
                    <option value="Self-Employed">Self-Employed</option>
                    <option value="Unemployed">Unemployed</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Section 3: Priority Eligibility Criteria (Toggles) */}
            <div className="pt-2">
              <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                <Briefcase size={15} className="text-cyan-500" />
                <span>3. Specific Category Status</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {/* Farmer Status */}
                <div className="border border-gray-200 rounded-xl p-3.5 flex items-center justify-between hover:bg-gray-50 transition">
                  <div>
                    <div className="text-sm font-semibold text-gray-900">Farmer / Landowner</div>
                    <div className="text-xs text-gray-500">Owns agricultural land or cultivates</div>
                  </div>
                  <select
                    name="farmer_status"
                    value={formData.farmer_status}
                    onChange={handleChange}
                    className="px-3 py-1.5 border border-gray-300 rounded-lg text-xs font-bold text-gray-800 focus:ring-2 focus:ring-cyan-500"
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                {/* Student Status */}
                <div className="border border-gray-200 rounded-xl p-3.5 flex items-center justify-between hover:bg-gray-50 transition">
                  <div>
                    <div className="text-sm font-semibold text-gray-900">Currently a Student</div>
                    <div className="text-xs text-gray-500">Enrolled in school, college or ITI</div>
                  </div>
                  <select
                    name="student_status"
                    value={formData.student_status}
                    onChange={handleChange}
                    className="px-3 py-1.5 border border-gray-300 rounded-lg text-xs font-bold text-gray-800 focus:ring-2 focus:ring-cyan-500"
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                {/* Disability Status */}
                <div className="border border-gray-200 rounded-xl p-3.5 flex items-center justify-between hover:bg-gray-50 transition">
                  <div>
                    <div className="text-sm font-semibold text-gray-900">Person with Disability</div>
                    <div className="text-xs text-gray-500">Divyangjan / Special category</div>
                  </div>
                  <select
                    name="disability_status"
                    value={formData.disability_status}
                    onChange={handleChange}
                    className="px-3 py-1.5 border border-gray-300 rounded-lg text-xs font-bold text-gray-800 focus:ring-2 focus:ring-cyan-500"
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-4">
              <button
                type="submit"
                disabled={loading}
                className="w-full sm:w-auto px-8 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white rounded-xl font-bold text-base shadow-md hover:shadow-lg transition flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <span className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></span>
                    <span>Analyzing with ML Model...</span>
                  </>
                ) : (
                  <>
                    <Search size={18} />
                    <span>Get AI Scheme Recommendations</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Results Section */}
        {results && (
          <div id="results-section" className="space-y-6 pt-4">
            {/* Results Header Bar */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <Award className="text-cyan-600" />
                  <span>Recommended Schemes for You</span>
                </h3>
                <p className="text-xs text-gray-500 mt-1">
                  Evaluated {results.totalSchemes} national schemes •{' '}
                  <span className="font-semibold text-green-600">
                    {results.eligibleCount} Eligible Matches Found
                  </span>
                </p>
              </div>

              {/* Filter Tabs */}
              <div className="flex flex-wrap gap-1.5">
                {[
                  { id: 'all', label: 'All Schemes' },
                  { id: 'eligible', label: '100% Eligible' },
                  { id: 'high', label: 'Top ML Match (≥80%)' },
                  { id: 'farmer', label: 'Farmer' },
                  { id: 'student', label: 'Student' }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveFilter(tab.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      activeFilter === tab.id
                        ? 'bg-cyan-500 text-white shadow-sm'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Scheme Cards Grid */}
            {filteredSchemes.length === 0 ? (
              <div className="bg-white rounded-2xl border border-gray-200 p-12 text-center">
                <AlertCircle size={40} className="mx-auto text-gray-400 mb-3" />
                <h4 className="text-base font-bold text-gray-700">No schemes found in this filter</h4>
                <p className="text-xs text-gray-500 mt-1">Try switching to "All Schemes" tab or updating income/age.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {filteredSchemes.map((scheme, idx) => {
                  const score = scheme.recommendationScore || 75;
                  const isEligible = scheme.isEligible !== false;

                  return (
                    <div
                      key={idx}
                      className={`bg-white rounded-2xl shadow-sm border transition hover:shadow-md flex flex-col justify-between overflow-hidden ${
                        isEligible ? 'border-gray-200' : 'border-amber-200 bg-amber-50/20'
                      }`}
                    >
                      <div className="p-6">
                        {/* Scheme Top Bar */}
                        <div className="flex items-start justify-between gap-3 mb-3">
                          <div>
                            <span className="inline-block px-2.5 py-0.5 rounded text-[11px] font-semibold bg-gray-100 text-gray-700 mb-1">
                              {scheme.department || 'Government of India'}
                            </span>
                            <h4 className="text-lg font-bold text-gray-900 leading-snug">
                              {scheme.scheme_name}
                            </h4>
                          </div>

                          {/* Score Badge */}
                          <div
                            className={`flex flex-col items-center justify-center px-3 py-1.5 rounded-xl border text-center flex-shrink-0 ${
                              score >= 80
                                ? 'bg-green-50 border-green-200 text-green-700'
                                : score >= 65
                                ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
                                : 'bg-gray-50 border-gray-200 text-gray-700'
                            }`}
                          >
                            <span className="text-lg font-extrabold leading-none">{score}%</span>
                            <span className="text-[10px] font-semibold uppercase mt-0.5">Match</span>
                          </div>
                        </div>

                        {/* Description */}
                        <p className="text-xs text-gray-600 mb-4 line-clamp-2">
                          {scheme.description}
                        </p>

                        {/* Benefits Highlight */}
                        {scheme.benefits && (
                          <div className="bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-100 rounded-xl p-3 mb-4 flex items-center gap-2">
                            <span className="text-emerald-700 font-bold text-sm">💰 Benefits:</span>
                            <span className="text-xs font-semibold text-emerald-900">
                              {scheme.benefits}
                            </span>
                          </div>
                        )}

                        {/* Eligibility Match Tags */}
                        {scheme.explanation && scheme.explanation.length > 0 && (
                          <div className="mb-4">
                            <div className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1.5">
                              Why You Qualify:
                            </div>
                            <div className="flex flex-wrap gap-1.5">
                              {scheme.explanation.map((exp, i) => (
                                <span
                                  key={i}
                                  className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-md text-[11px] font-medium bg-cyan-50 text-cyan-800 border border-cyan-100"
                                >
                                  <CheckCircle size={11} className="text-cyan-600" />
                                  <span>{exp}</span>
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Required Documents */}
                        {scheme.required_documents && (
                          <div className="text-xs text-gray-500 mb-2">
                            <span className="font-semibold text-gray-700">Documents: </span>
                            <span>{scheme.required_documents}</span>
                            {scheme.required_certificates && (
                              <span>, {scheme.required_certificates}</span>
                            )}
                          </div>
                        )}
                      </div>

                      {/* Card Footer Actions */}
                      <div className="bg-gray-50 border-t border-gray-100 px-6 py-3 flex items-center justify-between">
                        <button
                          type="button"
                          onClick={() => setSelectedScheme(scheme)}
                          className="text-xs font-bold text-cyan-600 hover:text-cyan-800 transition flex items-center gap-1"
                        >
                          <span>View Full Details</span>
                          <ChevronRight size={14} />
                        </button>

                        {scheme.official_website && (
                          <a
                            href={scheme.official_website}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-gray-900 hover:bg-cyan-600 text-white rounded-lg text-xs font-bold transition shadow-sm"
                          >
                            <span>Apply Official Portal</span>
                            <ExternalLink size={12} />
                          </a>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Scheme Detail Modal */}
        {selectedScheme && (
          <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl max-w-xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 sm:p-8">
              <div className="flex items-start justify-between border-b border-gray-100 pb-4 mb-4">
                <div>
                  <span className="text-xs font-bold text-cyan-600 uppercase tracking-wider">
                    {selectedScheme.department}
                  </span>
                  <h3 className="text-xl font-bold text-gray-900 mt-1">
                    {selectedScheme.scheme_name}
                  </h3>
                </div>
                <button
                  onClick={() => setSelectedScheme(null)}
                  className="p-1 rounded-lg text-gray-400 hover:text-gray-700 hover:bg-gray-100"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4 text-sm text-gray-700">
                <div>
                  <h5 className="font-bold text-gray-900 mb-1">Description</h5>
                  <p className="text-gray-600">{selectedScheme.description}</p>
                </div>

                <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3.5">
                  <h5 className="font-bold text-emerald-900 mb-0.5">Scheme Benefits</h5>
                  <p className="text-emerald-800 font-semibold">{selectedScheme.benefits}</p>
                </div>

                <div className="grid grid-cols-2 gap-3 bg-gray-50 p-3.5 rounded-xl text-xs">
                  <div>
                    <span className="font-semibold text-gray-500 block">Age Range:</span>
                    <span className="font-bold text-gray-800">
                      {selectedScheme.min_age || 0} to {selectedScheme.max_age || 100} Years
                    </span>
                  </div>
                  <div>
                    <span className="font-semibold text-gray-500 block">Income Limit:</span>
                    <span className="font-bold text-gray-800">
                      {selectedScheme.income_limit === 'unlimited'
                        ? 'No Limit'
                        : `Up to ₹${selectedScheme.income_limit}`}
                    </span>
                  </div>
                  <div>
                    <span className="font-semibold text-gray-500 block">Target Category:</span>
                    <span className="font-bold text-gray-800">{selectedScheme.category || 'All'}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-gray-500 block">Applicable Region:</span>
                    <span className="font-bold text-gray-800">{selectedScheme.state || 'All States'}</span>
                  </div>
                </div>

                <div>
                  <h5 className="font-bold text-gray-900 mb-1">Required Documents</h5>
                  <p className="text-gray-600">
                    {selectedScheme.required_documents || 'Aadhaar Card, Bank Passbook'}
                    {selectedScheme.required_certificates && `, ${selectedScheme.required_certificates}`}
                  </p>
                </div>

                {selectedScheme.last_application_date && (
                  <div className="text-xs text-gray-500">
                    <span className="font-semibold">Application Deadline: </span>
                    <span>{selectedScheme.last_application_date}</span>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-4 border-t border-gray-100 flex items-center justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setSelectedScheme(null)}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-xs font-semibold text-gray-700 hover:bg-gray-50"
                >
                  Close
                </button>
                {selectedScheme.official_website && (
                  <a
                    href={selectedScheme.official_website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-1.5 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg text-xs font-bold transition shadow-sm"
                  >
                    <span>Visit Official Website</span>
                    <ExternalLink size={13} />
                  </a>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
