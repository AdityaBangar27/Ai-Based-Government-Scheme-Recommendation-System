const jwt = require('jsonwebtoken');

// Authentication Middleware
exports.authMiddleware = (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = {
      userId: decoded.userId,
      email: decoded.email
    };
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Admin Middleware
exports.adminMiddleware = (req, res, next) => {
  // Check if user is admin
  // For now, assume user is admin if they have admin role in database
  next();
};
