import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth Service
export const authService = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout')
};

// User Service
export const userService = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  getProfileCompletion: () => api.get('/users/profile-completion'),
  uploadDocument: (formData) => api.post('/users/upload-document', formData)
};

// Scheme Service
export const schemeService = {
  getAllSchemes: () => api.get('/schemes'),
  getSchemeById: (id) => api.get(`/schemes/${id}`),
  searchSchemes: (query) => api.get(`/schemes/search/${query}`),
  filterSchemes: (filters) => api.post('/schemes/filter', filters)
};

// Recommendation Service
export const recommendationService = {
  getRecommendations: (data) => api.post('/recommendations/predict', data || {}),
  predictSchemes: (data) => api.post('/recommendations/predict', data || {}),
  compareSchemes: (schemeIds) => api.post('/recommendations/compare', { schemeIds }),
  getRecommendationDetails: (schemeId) => api.get(`/recommendations/${schemeId}`),
  getModelMetrics: () => api.get('/recommendations/model-metrics')
};

// Favorite Service
export const favoriteService = {
  addFavorite: (schemeId, schemeName) => api.post('/favorites/add', { schemeId, schemeName }),
  getFavorites: () => api.get('/favorites'),
  removeFavorite: (favoriteId) => api.delete(`/favorites/${favoriteId}`)
};

// Notification Service
export const notificationService = {
  getNotifications: () => api.get('/notifications'),
  markAsRead: (notificationId) => api.put(`/notifications/${notificationId}/read`),
  deleteNotification: (notificationId) => api.delete(`/notifications/${notificationId}`)
};

// Chatbot Service
export const chatbotService = {
  chat: (message) => api.post('/chatbot/message', { message })
};

// Admin Service
export const adminService = {
  getStats: () => api.get('/admin/stats'),
  getUserManagement: () => api.get('/admin/users'),
  getSchemeManagement: () => api.get('/admin/schemes'),
  uploadCSV: (formData) => api.post('/admin/upload-csv', formData),
  retrainModel: () => api.post('/admin/retrain-model'),
  viewLogs: () => api.get('/admin/logs')
};

export default api;
