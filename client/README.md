# 💻 Frontend Web Client Application Process

## Overview
The frontend is a single-page web application built with **React 18** and styled using **Tailwind CSS**. It provides citizens with an intuitive, accessible portal to enter demographic criteria, receive AI-driven scheme recommendations, compare scheme benefits, and inspect model transparency metrics.

---

## 📁 Directory Structure

```
client/
├── README.md               # This process guide
├── package.json            # React dependencies & build scripts
├── tailwind.config.js      # Tailwind CSS styling configuration
├── public/                 # Static assets & HTML root
│   └── index.html
└── src/                    # Application source code
    ├── App.js              # Application router & toast provider
    ├── index.js            # React DOM mounting point
    ├── components/         # Reusable UI components
    │   ├── Chatbot.js      # Citizen AI assistant widget
    │   ├── Footer.js       # Global footer
    │   └── Navbar.js       # Top navigation bar
    ├── pages/              # Primary route views
    │   ├── Home.js         # Main recommendation portal & profile form
    │   ├── Dashboard.js    # Citizen personal dashboard
    │   ├── Profile.js      # User profile manager
    │   ├── Recommendations.js # Standalone recommendations page
    │   ├── SchemeDetails.js   # Detailed scheme view
    │   ├── NotFound.js     # 404 handler
    │   ├── Admin/          # Administrative analytics views
    │   │   └── Dashboard.js
    │   └── Auth/           # Authentication forms
    │       ├── Login.js
    │       └── Register.js
    ├── services/           # Network & API layer
    │   └── api.js          # Axios client with JWT interceptor
    └── styles/             # Global stylesheets
        ├── index.css
        └── tailwind.css
```

---

## 🚀 Execution & Scripts

```bash
cd client
npm install

# Start local development server (Port 3000)
npm start

# Build production bundle for deployment
npm run build
```

---

## 🧭 Citizen User Journey & Processes

### 1. Demographic Profile Input Process (`Home.js`)
- Citizens can manually enter or adjust 11 key demographic fields:
  - Age, Annual Income, Gender, Occupation, Education, Caste Category, State, Disability Status, Farmer Status, Student Status, Employment Status.
- **Quick-Fill Demo Presets**: One-click autofill buttons for representative citizen archetypes:
  - 🌾 *Small Farmer* (Maharashtra, Agriculture)
  - 🎓 *College Student* (Delhi, Education & Scholarships)
  - 🛠️ *Rural Artisan* (Uttar Pradesh, MSME)
  - 💼 *Unorganized Worker* (General, Labor & Pension)

### 2. AI Recommendation Generation Process
- When submitted, the form invokes `recommendationService.getRecommendations()`.
- Smooth auto-scrolls to the results section upon receipt.
- Filters allow tabbed views:
  - *All Schemes*
  - *100% Eligible*
  - *Top ML Match (≥80%)*
  - *Farmer Schemes*
  - *Student Scholarships*
- Each card displays:
  - Match score badge (e.g. `96% Match`)
  - Department and scheme title
  - High-level benefit summary (e.g. `₹6,000 annually`)
  - "Why You Qualify" verification badges
  - Required documents and certificates
  - Action buttons: Modal detail dialog & Direct link to official government portal.

### 3. Scheme Details Modal
- An accessible modal dialog showing full scheme description, eligibility boundaries, required documentation, and direct application links.

### 4. Interactive Chatbot Assistant (`Chatbot.js`)
- Floating chat assistant available on every page to answer eligibility questions and clarify required certificates.

---

## 🎨 Design System & Accessibility
- **Responsive**: Fully optimized for mobile phones, tablets, and desktop displays.
- **Color Palette**: High-contrast, citizen-friendly palette featuring cyan, emerald, and slate.
- **Icons**: Lightweight vector icons powered by `react-feather`.
- **Notifications**: Instant feedback using `react-toastify`.

