const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { createObjectCsvWriter } = require('csv-writer');

const favoritesFile = path.join(__dirname, '../../datasets/favorites.csv');

// Add Favorite
exports.addFavorite = async (req, res) => {
  try {
    const { userId } = req.user;
    const { schemeId, schemeName } = req.body;

    const favorites = [];
    fs.createReadStream(favoritesFile)
      .pipe(csv())
      .on('data', (data) => favorites.push(data))
      .on('end', async () => {
        const newFavorite = {
          favorite_id: Date.now().toString(),
          user_id: userId,
          scheme_id: schemeId,
          scheme_name: schemeName,
          added_at: new Date().toISOString(),
          removed_at: '',
          is_active: 'true'
        };

        favorites.push(newFavorite);

        const writer = createObjectCsvWriter({
          path: favoritesFile,
          header: Object.keys(newFavorite).map(key => ({ id: key, title: key }))
        });
        await writer.writeRecords(favorites);

        res.json({
          message: 'Favorite added successfully',
          favorite: newFavorite
        });
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Remove Favorite
exports.removeFavorite = async (req, res) => {
  try {
    const { userId } = req.user;
    const { favoriteId } = req.params;

    res.json({ message: 'Favorite removed successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Get Favorites
exports.getFavorites = (req, res) => {
  try {
    const { userId } = req.user;
    const favorites = [];

    fs.createReadStream(favoritesFile)
      .pipe(csv())
      .on('data', (data) => {
        if (data.user_id === userId && data.is_active === 'true') {
          favorites.push(data);
        }
      })
      .on('end', () => {
        res.json(favorites);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
