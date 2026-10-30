# 🌐 Backend API Server Process

## Overview
The backend application is a robust **RESTful API** built with **Node.js** and **Express.js**. It provides authentication, scheme catalog retrieval, recommendation generation via Python IPC, administrative operations, and user profile management with zero external database dependencies (using structured CSV flat-file persistence).

---

## 📁 Directory Structure

```
server/
├── README.md               # This process guide
├── server.js               # Application entry point & middleware setup
├── package.json            # Node.js dependencies & scripts
├── .env                    # Runtime configuration (PORT, JWT_SECRET, paths)
├── controllers/            # Request handlers & business logic
│   ├── adminController.js
│   ├── authController.js
│   ├── chatbotController.js
│   ├── favoriteController.js
│   ├── notificationController.js
│   ├── recommendationController.js
│   ├── schemeController.js
│   └── userController.js
├── middleware/             # Express middlewares
│   └── auth.js             # JWT authentication & route protection
└── routes/                 # Express route definitions
    ├── adminRoutes.js
    ├── authRoutes.js
    ├── chatbotRoutes.js
    ├── favoriteRoutes.js
    ├── notificationRoutes.js
    ├── recommendationRoutes.js
    ├── schemeRoutes.js
    └── userRoutes.js
```

---

## 🚀 Execution & Lifecycle

### Installation & Startup
```bash
cd server
npm install

# Development mode (auto-reload via nodemon)
npm run dev

# Production startup
npm start
```

### Environment Configuration (`.env`)
```ini
PORT=5000
NODE_ENV=development
CLIENT_URL=http://localhost:3000
JWT_SECRET=your_jwt_secret_key_change_this
JWT_EXPIRE=7d
BCRYPT_ROUNDS=10
ML_MODEL_PATH=../ml_model/scheme_model.pkl
ENCODERS_PATH=../ml_model/encoders.pkl
```

---

## 📡 API Endpoint Processes

### 1. Recommendation Process (`/api/recommendations`)
- **`POST /api/recommendations/predict`**: Accepts citizen demographic parameters (`age`, `income`, `occupation`, `state`, `category`, etc.).
  - Evaluates rule-based eligibility checks (age boundaries, income caps).
  - Submits features to Python ML script (`ml_model/predict.py`) via `child_process.spawn()`.
  - Merges ML probabilities (60% weight) with eligibility criteria scores (40% weight).
  - Returns sorted array of matching schemes with match percentages and justification explanations.
- **`GET /api/recommendations/model-metrics`**: Returns multi-model benchmarks, Random Forest accuracy/F1 metrics, and Gini feature importances.

### 2. Authentication Process (`/api/auth`)
- **`POST /api/auth/register`**: Validates input, hashes password using `bcryptjs` (10 rounds), and appends user record to `datasets/users.csv`.
- **`POST /api/auth/login`**: Authenticates credentials and returns a signed `jsonwebtoken` (7-day validity).

### 3. Scheme Management Process (`/api/schemes`)
- **`GET /api/schemes`**: Reads and returns all government schemes from `datasets/schemes.csv`.
- **`GET /api/schemes/:id`**: Returns specific scheme details.
- **`GET /api/schemes/search/:query`**: Keyword search across titles, departments, and benefits.

### 4. Chatbot Process (`/api/chatbot`)
- **`POST /api/chatbot/message`**: Rule and keyword-guided citizen assistant answering questions regarding document requirements, eligibility, deadlines, and portal navigation.

### 5. Health Check Process (`/api/health`)
- **`GET /api/health`**: Returns system uptime, active status, and server timestamp.

---

## 🛡️ Security & Reliability
- **Helmet.js**: Sets secure HTTP response headers.
- **CORS**: Restricts API calls to authorized frontend origins.
- **Graceful ML Fallback**: If Python is unavailable, recommendation calculations seamlessly fallback to rule-based filtering.

