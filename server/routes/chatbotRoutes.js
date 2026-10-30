const express = require('express');
const router = express.Router();
const { chat } = require('../controllers/chatbotController');
const { authMiddleware } = require('../middleware/authMiddleware');

// Protected Routes
router.post('/message', authMiddleware, chat);

module.exports = router;
