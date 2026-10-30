const express = require('express');
const router = express.Router();
const { addFavorite, removeFavorite, getFavorites } = require('../controllers/favoriteController');
const { authMiddleware } = require('../middleware/authMiddleware');

// Protected Routes
router.post('/add', authMiddleware, addFavorite);
router.delete('/:favoriteId', authMiddleware, removeFavorite);
router.get('/', authMiddleware, getFavorites);

module.exports = router;
