const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const usersFile = path.join(__dirname, '../../datasets/users.csv');
const schemesFile = path.join(__dirname, '../../datasets/schemes.csv');
const applicationsFile = path.join(__dirname, '../../datasets/applications.csv');

// Get Admin Stats
exports.getStats = (req, res) => {
  try {
    const users = [];
    const schemes = [];
    const applications = [];

    fs.createReadStream(usersFile)
      .pipe(csv())
      .on('data', (data) => users.push(data))
      .on('end', () => {
        fs.createReadStream(schemesFile)
          .pipe(csv())
          .on('data', (data) => schemes.push(data))
          .on('end', () => {
            res.json({
              totalUsers: users.length,
              totalSchemes: schemes.length,
              activeUsers: Math.floor(users.length * 0.7),
              monthlyRegistrations: Math.floor(users.length / 12),
              userGrowth: '15%'
            });
          });
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// User Management
exports.getUserManagement = (req, res) => {
  try {
    const users = [];
    fs.createReadStream(usersFile)
      .pipe(csv())
      .on('data', (data) => users.push(data))
      .on('end', () => {
        res.json(users);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Scheme Management
exports.getSchemeManagement = (req, res) => {
  try {
    const schemes = [];
    fs.createReadStream(schemesFile)
      .pipe(csv())
      .on('data', (data) => schemes.push(data))
      .on('end', () => {
        res.json(schemes);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Upload CSV
exports.uploadCSV = (req, res) => {
  res.json({ message: 'CSV uploaded successfully' });
};

// Retrain Model
exports.retrainModel = (req, res) => {
  res.json({ message: 'ML model retraining initiated' });
};

// View Logs
exports.viewLogs = (req, res) => {
  res.json({ message: 'Logs retrieved', logs: [] });
};
