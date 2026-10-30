const express = require('express');
const router = express.Router();
const { 
  getStats, 
  getUserManagement, 
  getSchemeManagement,
  uploadCSV,
  retrainModel,
  viewLogs
} = require('../controllers/adminController');
const { authMiddleware, adminMiddleware } = require('../middleware/authMiddleware');

// Protected Admin Routes
router.get('/stats', authMiddleware, adminMiddleware, getStats);
router.get('/users', authMiddleware, adminMiddleware, getUserManagement);
router.get('/schemes', authMiddleware, adminMiddleware, getSchemeManagement);
router.post('/upload-csv', authMiddleware, adminMiddleware, uploadCSV);
router.post('/retrain-model', authMiddleware, adminMiddleware, retrainModel);
router.get('/logs', authMiddleware, adminMiddleware, viewLogs);

module.exports = router;
