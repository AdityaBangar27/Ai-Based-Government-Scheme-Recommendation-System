const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { createObjectCsvWriter } = require('csv-writer');

const notificationsFile = path.join(__dirname, '../../datasets/notifications.csv');

// Get Notifications
exports.getNotifications = (req, res) => {
  try {
    const { userId } = req.user;
    const notifications = [];

    fs.createReadStream(notificationsFile)
      .pipe(csv())
      .on('data', (data) => {
        if (data.user_id === userId) {
          notifications.push(data);
        }
      })
      .on('end', () => {
        res.json(notifications);
      });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Mark as Read
exports.markAsRead = async (req, res) => {
  try {
    const { notificationId } = req.params;
    res.json({ message: 'Notification marked as read' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Delete Notification
exports.deleteNotification = async (req, res) => {
  try {
    const { notificationId } = req.params;
    res.json({ message: 'Notification deleted' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
