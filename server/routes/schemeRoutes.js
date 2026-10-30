const express = require('express');
const router = express.Router();
const { getAllSchemes, getSchemeById, searchSchemes, filterSchemes } = require('../controllers/schemeController');

// Public Routes
router.get('/', getAllSchemes);
router.get('/:id', getSchemeById);
router.get('/search/:query', searchSchemes);
router.post('/filter', filterSchemes);

module.exports = router;
