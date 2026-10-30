const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { createObjectCsvWriter } = require('csv-writer');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const usersFile = path.join(__dirname, '../../datasets/users.csv');

// Register User
exports.register = async (req, res) => {
  try {
    const { full_name, email, password, confirm_password } = req.body;

    if (password !== confirm_password) {
      return res.status(400).json({ error: 'Passwords do not match' });
    }

    // Check if user already exists
    const users = [];
    fs.createReadStream(usersFile)
      .pipe(csv())
      .on('data', (data) => users.push(data))
      .on('end', async () => {
        const userExists = users.some(u => u.email === email);
        if (userExists) {
          return res.status(400).json({ error: 'User already exists' });
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);
        const userId = Date.now().toString();

        // Create new user
        const newUser = {
          user_id: userId,
          full_name,
          email,
          password: hashedPassword,
          mobile_number: '',
          aadhaar_number: '',
          pan_number: '',
          date_of_birth: '',
          age: '',
          gender: '',
          state: '',
          district: '',
          taluka: '',
          village: '',
          address: '',
          occupation: '',
          education: '',
          annual_income: '',
          category: '',
          religion: '',
          disability_status: '',
          farmer_status: '',
          student_status: '',
          employment_status: '',
          marital_status: '',
          bank_name: '',
          bank_account_number: '',
          ifsc_code: '',
          profile_image: '',
          profile_completion_percentage: 20,
          created_at: new Date().toISOString(),
          recommended_scheme: ''
        };

        // Read existing data
        let allUsers = [];
        fs.createReadStream(usersFile)
          .pipe(csv())
          .on('data', (data) => allUsers.push(data))
          .on('end', async () => {
            allUsers.push(newUser);
            // Write to CSV
            const writer = createObjectCsvWriter({
              path: usersFile,
              header: Object.keys(newUser).map(key => ({ id: key, title: key }))
            });
            await writer.writeRecords(allUsers);

            // Generate JWT
            const token = jwt.sign({ userId, email }, process.env.JWT_SECRET, {
              expiresIn: process.env.JWT_EXPIRE
            });

            res.status(201).json({
              message: 'User registered successfully',
              token,
              user: { userId, email, full_name }
            });
          });
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Login User
exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find user
    const users = [];
    fs.createReadStream(usersFile)
      .pipe(csv())
      .on('data', (data) => users.push(data))
      .on('end', async () => {
        const user = users.find(u => u.email === email);
        if (!user) {
          return res.status(401).json({ error: 'Invalid credentials' });
        }

        // Compare password
        const isValid = await bcrypt.compare(password, user.password);
        if (!isValid) {
          return res.status(401).json({ error: 'Invalid credentials' });
        }

        // Generate JWT
        const token = jwt.sign(
          { userId: user.user_id, email: user.email },
          process.env.JWT_SECRET,
          { expiresIn: process.env.JWT_EXPIRE }
        );

        res.json({
          message: 'Login successful',
          token,
          user: {
            userId: user.user_id,
            email: user.email,
            full_name: user.full_name
          }
        });
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Logout
exports.logout = (req, res) => {
  res.json({ message: 'Logout successful' });
};

// Forgot Password
exports.forgotPassword = (req, res) => {
  res.json({ message: 'Password reset email sent' });
};

// Reset Password
exports.resetPassword = (req, res) => {
  res.json({ message: 'Password reset successful' });
};
