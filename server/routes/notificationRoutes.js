const express = require('express');
const router = express.Router();
const { getNotifications, markAsRead, deleteNotification } = require('../controllers/notificationController');
const { authMiddleware } = require('../middleware/authMiddleware');

// Protected Routes
router.get('/', authMiddleware, getNotifications);
router.put('/:notificationId/read', authMiddleware, markAsRead);
router.delete('/:notificationId', authMiddleware, deleteNotification);

module.exports = router;
