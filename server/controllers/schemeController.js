const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

const schemesFile = path.join(__dirname, '../../datasets/schemes.csv');

// Get All Schemes
exports.getAllSchemes = (req, res) => {
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

// Get Scheme By ID
exports.getSchemeById = (req, res) => {
  try {
    const { id } = req.params;
    const schemes = [];

    fs.createReadStream(schemesFile)
      .pipe(csv())
      .on('data', (data) => schemes.push(data))
      .on('end', () => {
        const scheme = schemes.find(s => s.scheme_id === id);
        if (!scheme) {
          return res.status(404).json({ error: 'Scheme not found' });
        }
        res.json(scheme);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Search Schemes
exports.searchSchemes = (req, res) => {
  try {
    const { query } = req.params;
    const schemes = [];

    fs.createReadStream(schemesFile)
      .pipe(csv())
      .on('data', (data) => schemes.push(data))
      .on('end', () => {
        const results = schemes.filter(s =>
          s.scheme_name.toLowerCase().includes(query.toLowerCase()) ||
          s.description.toLowerCase().includes(query.toLowerCase())
        );
        res.json(results);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Filter Schemes
exports.filterSchemes = (req, res) => {
  try {
    const { category, state, minIncome, maxIncome } = req.body;
    const schemes = [];

    fs.createReadStream(schemesFile)
      .pipe(csv())
      .on('data', (data) => schemes.push(data))
      .on('end', () => {
        let filtered = schemes;

        if (category) {
          filtered = filtered.filter(s => s.category === category);
        }
        if (state) {
          filtered = filtered.filter(s => s.state === state || s.state === 'All States');
        }

        res.json(filtered);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
