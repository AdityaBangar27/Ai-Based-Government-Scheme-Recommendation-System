# Quick Start Guide

## Installation & Setup

### Step 1: Install Backend Dependencies

```bash
cd server
npm install
```

### Step 2: Configure Backend Environment

Create `.env` file:

```env
PORT=5000
JWT_SECRET=your-super-secret-key-change-this
JWT_EXPIRE=7d
BCRYPT_ROUNDS=10
CLIENT_URL=http://localhost:3000
NODE_ENV=development

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# ML Model Paths
ML_MODEL_PATH=../ml_model/scheme_model.pkl
ENCODERS_PATH=../ml_model/encoders.pkl

# File Upload
MAX_FILE_SIZE=5242880
UPLOAD_PATH=../uploads
```

### Step 3: Start Backend Server

```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm start
```

Backend will run on: **http://localhost:5000**

### Step 4: Install Frontend Dependencies

```bash
cd client
npm install
```

### Step 5: Start Frontend

```bash
npm start
```

Frontend will run on: **http://localhost:3000**

### Step 6: Set up ML Model

```bash
cd ml_model
pip install -r requirements.txt

# Train the model (one-time)
python train_model.py

# This creates:
# - ../models/scheme_model.pkl
# - ../models/encoders.pkl
# - ../models/model_config.json
```

---

## Testing the Application

### 1. Register a New User
- Go to http://localhost:3000/register
- Fill in the form
- Click "Create Account"

### 2. Login
- Use your registered email and password
- Click "Login"

### 3. Complete Profile
- Go to Profile page
- Fill in additional details (Age, Income, State, etc.)
- The profile completion percentage increases

### 4. Get Recommendations
- Go to "Recommendations" or "Dashboard"
- System fetches eligible schemes based on your profile

### 5. Admin Panel
- Create an admin user in admins.csv
- Login with admin account
- Access /admin for analytics

---

## API Testing with Curl

### Register
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Get Schemes
```bash
curl http://localhost:5000/api/schemes
```

### Get Recommendations (Authenticated)
```bash
curl -X POST http://localhost:5000/api/recommendations/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

---

## Environment Variables Explained

| Variable | Purpose | Default |
|----------|---------|---------|
| PORT | Server port | 5000 |
| JWT_SECRET | Secret key for JWT tokens | - |
| CLIENT_URL | Frontend URL | http://localhost:3000 |
| ML_MODEL_PATH | Path to ML model file | ../ml_model/scheme_model.pkl |
| UPLOAD_PATH | Upload directory for documents | ../uploads |

---

## Troubleshooting

### ❌ "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### ❌ "Module not found"
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### ❌ "ML Model not found"
```bash
# Retrain the model
cd ml_model
python train_model.py
```

### ❌ CORS Error
Check that CLIENT_URL in `.env` matches your frontend URL

### ❌ Database Connection Error
Make sure CSV files exist in `../datasets/` directory

---

## File Structure After Setup

```
government-scheme-recommendation/
├── client/                    # Frontend React app
│   ├── node_modules/
│   ├── src/
│   ├── public/
│   └── package.json
├── server/                    # Backend Express server
│   ├── node_modules/
│   ├── controllers/
│   ├── routes/
│   ├── middleware/
│   ├── package.json
│   ├── .env
│   └── server.js
├── ml_model/                  # ML models
│   ├── train_model.py
│   ├── predict.py
│   └── requirements.txt
├── models/                    # Saved models (created after training)
│   ├── scheme_model.pkl
│   ├── encoders.pkl
│   └── model_config.json
├── datasets/                  # CSV data files
│   ├── users.csv
│   ├── schemes.csv
│   ├── login.csv
│   ├── favorites.csv
│   ├── notifications.csv
│   ├── applications.csv
│   ├── documents.csv
│   ├── feedback.csv
│   ├── chat_history.csv
│   ├── admins.csv
│   └── email_logs.csv
├── uploads/                   # User uploaded documents
└── README.md
```

---

## Development Tips

### Hot Reload
- Backend: nodemon automatically restarts on file changes
- Frontend: React dev server auto-refreshes

### Debugging
- Backend: Check `node_modules/.bin/nodemon --inspect server.js`
- Frontend: Use React Developer Tools extension

### Data Persistence
- All data stored in CSV files
- CSV files in `datasets/` folder
- Easy to migrate to MongoDB later

### API Testing
- Use Postman collection (import from docs)
- Or test with curl commands above

---

## Next Steps

1. ✅ Complete profile with your details
2. ✅ Get scheme recommendations
3. ✅ Explore schemes you're eligible for
4. ✅ Create admin user for analytics
5. ✅ Customize the UI as needed

---

## Need Help?

- Check API logs in terminal
- Review error messages in browser console
- Check `.env` configuration
- Ensure all dependencies installed with `npm install`

---

**Happy coding! 🚀**
