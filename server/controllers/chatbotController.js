const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const { createObjectCsvWriter } = require('csv-writer');

const chatHistoryFile = path.join(__dirname, '../../datasets/chat_history.csv');
const schemesFile = path.join(__dirname, '../../datasets/schemes.csv');

// Chatbot Responses Knowledge Base
const chatbotKB = {
  'pm kisan': 'PM Kisan Samman Nidhi provides ₹6000 annually to farmers. Eligibility: Be a farmer with land ownership.',
  'fasal bima': 'Pradhan Mantri Fasal Bima Yojana is a crop insurance scheme providing premium subsidy.',
  'scholarship': 'National Scholarship Scheme provides scholarships from ₹500-₹5000 monthly based on merit.',
  'awas': 'Pradhan Mantri Awas Yojana provides housing loans with subsidy for EWS and LIG categories.',
  'ayushman': 'Ayushman Bharat provides health insurance coverage of ₹5 lakh for poor families.',
  'disability': 'Various schemes support people with disabilities including financial assistance and employment.',
  'farmer': 'Multiple schemes available for farmers including PM Kisan, Fasal Bima, and Kisan Credit Card.',
  'woman': 'Beti Bachao Beti Padhao and other women-specific schemes provide educational and financial support.',
  'student': 'National Scholarship Scheme and educational support programs available for students.',
  'eligible': 'To check eligibility, complete your profile with age, income, occupation, and state information.',
  'documents': 'Required documents vary by scheme but generally include: Aadhar, Income Certificate, Bank Details.',
  'apply': 'You can apply for schemes through the official government portals. We provide direct links.'
};

// Chat Handler
exports.chat = async (req, res) => {
  try {
    const { userId } = req.user;
    const { message } = req.body;

    // Simple chatbot logic
    const lowerMessage = message.toLowerCase();
    let response = 'I am here to help! Ask me about government schemes, eligibility criteria, or documents needed.';

    // Search knowledge base
    for (const [key, value] of Object.entries(chatbotKB)) {
      if (lowerMessage.includes(key)) {
        response = value;
        break;
      }
    }

    // Save chat history
    const chatEntry = {
      chat_id: Date.now().toString(),
      user_id: userId,
      message,
      response,
      message_type: 'user',
      conversation_id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      created_at: new Date().toISOString()
    };

    res.json({
      message: 'Chat response generated',
      user_message: message,
      bot_response: response,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
