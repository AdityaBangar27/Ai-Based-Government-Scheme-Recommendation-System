const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { createObjectCsvWriter } = require('csv-writer');

const usersFile = path.join(__dirname, '../../datasets/users.csv');

// Get User Profile
exports.getProfile = async (req, res) => {
  try {
    const { userId } = req.user;
    const users = [];

    fs.createReadStream(usersFile)
      .pipe(csv())
      .on('data', (data) => users.push(data))
      .on('end', () => {
        const user = users.find(u => u.user_id === userId);
        if (!user) {
          return res.status(404).json({ error: 'User not found' });
        }
        res.json(user);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Update User Profile
exports.updateProfile = async (req, res) => {
  try {
    const { userId } = req.user;
    const updates = req.body;

    const users = [];
    fs.createReadStream(usersFile)
      .pipe(csv())
      .on('data', (data) => users.push(data))
      .on('end', async () => {
        const userIndex = users.findIndex(u => u.user_id === userId);
        if (userIndex === -1) {
          return res.status(404).json({ error: 'User not found' });
        }

        users[userIndex] = { ...users[userIndex], ...updates };
        
        const writer = createObjectCsvWriter({
          path: usersFile,
          header: Object.keys(users[0]).map(key => ({ id: key, title: key }))
        });
        await writer.writeRecords(users);

        res.json({
          message: 'Profile updated successfully',
          user: users[userIndex]
        });
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Upload Document
exports.uploadDocument = (req, res) => {
  res.json({ message: 'Document uploaded successfully' });
};

// Get Documents
exports.getDocuments = async (req, res) => {
  try {
    const { userId } = req.user;
    // Read documents.csv
    res.json({ message: 'Documents retrieved' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get Profile Completion
exports.getProfileCompletion = async (req, res) => {
  try {
    const { userId } = req.user;
    const users = [];

    fs.createReadStream(usersFile)
      .pipe(csv())
      .on('data', (data) => users.push(data))
      .on('end', () => {
        const user = users.find(u => u.user_id === userId);
        if (!user) {
          return res.status(404).json({ error: 'User not found' });
        }

        const completionPercentage = user.profile_completion_percentage || 0;
        const missingFields = [
          !user.mobile_number && 'Mobile Number',
          !user.aadhaar_number && 'Aadhaar',
          !user.state && 'State',
          !user.occupation && 'Occupation',
          !user.annual_income && 'Income'
        ].filter(Boolean);

        res.json({
          completionPercentage,
          missingFields
        });
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
