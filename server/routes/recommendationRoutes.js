const express = require('express');
const router = express.Router();
const {
  getRecommendations,
  compareSchemes,
  getRecommendationDetails,
  getModelMetrics
} = require('../controllers/recommendationController');

// Public Recommendation & Prediction Endpoints
router.post('/generate', getRecommendations);
router.post('/predict', getRecommendations);
router.post('/recommend', getRecommendations);

// Model Performance Metrics & Architecture Comparison
router.get('/model-metrics', getModelMetrics);

router.post('/compare', compareSchemes);
router.get('/:schemeId', getRecommendationDetails);

module.exports = router;
