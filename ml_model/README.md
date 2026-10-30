# 🤖 Machine Learning Model Process

## Overview
This module houses the **Random Forest Machine Learning Recommendation Engine** that powers the Government Scheme Recommendation System. It is responsible for training the classification model, serializing learned encoders and model weights, and providing a high-speed prediction interface invoked by the backend API.

---

## 📁 Directory Structure

```
ml_model/
├── README.md               # This process guide
├── requirements.txt        # Python package dependencies
├── train_model.py          # Model training pipeline
├── predict.py              # CLI inference engine (invoked by backend)
├── model_config.json       # Feature configuration & hyperparameters
├── scheme_model.pkl        # Serialized Random Forest classifier
└── encoders.pkl            # Serialized scikit-learn LabelEncoders
```

---

## ⚙️ Core Processes

### 1. Model Training Process (`train_model.py`)
The training script executes the full ML lifecycle:
1. **Data Ingestion**: Loads user demographic profiles and government scheme criteria.
2. **Feature Preparation**: Generates candidate user-scheme pairs validating eligibility constraints (age limits, income ceilings).
3. **Categorical Encoding**: Fits `LabelEncoder` instances for demographic fields:
   - `gender`, `occupation`, `education`, `category`, `state`
   - `disability_status`, `farmer_status`, `student_status`, `employment_status`
4. **Classifier Training**: Fits a `RandomForestClassifier` with:
   - `n_estimators = 100` (100 ensemble decision trees)
   - `max_depth = 15`
   - `min_samples_split = 5`
   - `min_samples_leaf = 2`
   - `random_state = 42`
5. **Evaluation**: Computes Train/Test Accuracy, Weighted Precision, Recall, and F1-Score.
6. **Artifact Export**: Saves `scheme_model.pkl`, `encoders.pkl`, and `model_config.json`.

```bash
# Run training pipeline
python train_model.py
```

### 2. Prediction Process (`predict.py`)
`predict.py` acts as the microservice bridge between the Node.js Express backend and Python:
- Receives a JSON-encoded citizen demographic profile via standard input / command-line argument.
- Loads pre-trained model and encoders.
- Transforms and encodes categorical attributes matching the training feature space.
- Calls `predict_proba()` to compute probability distributions across all available schemes.
- Returns a ranked list of recommended schemes with confidence percentages as structured JSON to stdout.

```bash
# Manual CLI test
python predict.py '{"age": 30, "income": 120000, "occupation": "Farmer", "category": "OBC", "state": "Maharashtra"}'
```

---

## 📊 Features & Model Configuration

| Feature Name | Type | Description |
|---|---|---|
| `age` | Integer | Citizen age (years) |
| `income` | Float / Int | Annual household income in ₹ (INR) |
| `gender` | Categorical | Male, Female, Other |
| `occupation` | Categorical | Farmer, Student, Artisan, Unorganized Worker, etc. |
| `education` | Categorical | 10th Pass, 12th Pass, Graduate, Post Graduate, etc. |
| `category` | Categorical | General, OBC, SC, ST, EWS |
| `state` | Categorical | Indian State / UT |
| `disability_status` | Binary | Yes / No |
| `farmer_status` | Binary | Yes / No |
| `student_status` | Binary | Yes / No |
| `employment_status`| Categorical | Employed, Self-Employed, Unemployed |

---

## 🔌 Integration with Express Backend
The Express server spawns `predict.py` via Node.js `child_process.spawn()` inside `server/controllers/recommendationController.js`:

```javascript
const pyProcess = spawn('python', [pythonScript, JSON.stringify(userFeatures)], {
  cwd: path.join(__dirname, '../../ml_model'),
  env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
});
```

If Python execution exceeds 4 seconds or fails, the backend falls back to rule-based eligibility evaluation, ensuring 100% portal uptime.

