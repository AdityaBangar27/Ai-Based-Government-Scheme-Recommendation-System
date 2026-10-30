const express = require('express');
const router = express.Router();
const { getProfile, updateProfile, uploadDocument, getDocuments, getProfileCompletion } = require('../controllers/userController');
const { authMiddleware } = require('../middleware/authMiddleware');

// Protected Routes
router.get('/profile', authMiddleware, getProfile);
router.put('/profile', authMiddleware, updateProfile);
router.post('/upload-document', authMiddleware, uploadDocument);
router.get('/documents', authMiddleware, getDocuments);
router.get('/profile-completion', authMiddleware, getProfileCompletion);

module.exports = router;
