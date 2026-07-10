# AI-Based Government Scheme Recommendation System Using Random Forest

An end-to-end, production-ready machine learning recommendation engine designed to match and rank government schemes for citizens based on demographic, geographic, and economic attributes. This project is optimized for academic portfolios (B.Tech Final Year Projects), research papers, and professional software engineering repositories.

---

## Project Overview

Governments run numerous welfare schemes, but citizens often miss out due to a lack of awareness or difficulty in evaluating complex eligibility criteria. This system solves that problem by:
1. Evaluating exact rule-based eligibility matching across multiple parameters.
2. Training a **Random Forest Classifier** to learn matching patterns.
3. Ranking eligible schemes by predictive probability to output the **Top 5 Recommendations** for any user profile.

---

## Core Technologies
- **Backend / Machine Learning**: Python, Pandas, Numpy, Scikit-learn, Joblib
- **Visualization**: Matplotlib
- **Web Interface**: Flask, Bootstrap 5, Custom CSS3, HTML5

---

## Folder Structure

The project directory structure is laid out as follows:

```text
AI_Scheme_Recommendation/
│
├── users.csv                     # Raw user demographic dataset (1,500 records)
├── schemes.csv                   # Raw government scheme eligibility criteria (100 records)
│
├── data_cleaning.py              # Phase 2: Cleans raw datasets and normalizes values
├── create_training_dataset.py    # Phase 3: Evaluates rule-based eligibility mapping
├── feature_engineering.py        # Phase 4: Label encodes categorical columns
├── train_random_forest.py        # Phase 5: Trains base Random Forest Classifier
├── hyperparameter_tuning.py      # Phase 6: Optimizes model hyperparameters via GridSearchCV
├── evaluate_model.py             # Phase 7: Computes metrics and saves visualization plots
├── predict.py                    # Phase 8: Command-line prediction interface
├── app.py                        # Phase 9: Flask Web Application server
│
├── templates/
│   └── index.html                # Phase 10: Responsive dashboard interface
│
├── static/
│   └── style.css                 # Phase 11: Premium layout and animations
│
├── models/
│   ├── rf_model.pkl              # Base Random Forest Classifier
│   ├── best_rf_model.pkl         # Hyperparameter tuned Random Forest Classifier
│   └── encoder.pkl               # Serialized LabelEncoder dictionary for ML features
│
├── graphs/
│   ├── confusion_matrix.png      # Confusion Matrix plot (Top classes by support)
│   ├── feature_importance.png    # Feature Importance horizontal bar chart
│   ├── roc_curve.png             # Receiver Operating Characteristic plot
│   └── classification_report.txt # Text file containing the full evaluation report
│
├── cleaned_users.csv             # Cleaned user demographic dataset
├── cleaned_schemes.csv           # Cleaned scheme eligibility dataset
├── training_dataset.csv          # Mapped eligibility dataset
├── encoded_training_dataset.csv  # Final preprocessed dataset used for ML
│
├── requirements.txt              # Project dependencies list
├── LICENSE                       # MIT License file
└── README.md                     # Comprehensive documentation
```

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/AI_Scheme_Recommendation.git
   cd AI_Scheme_Recommendation
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then execute:
   ```bash
   pip install -r requirements.txt
   ```

---

## Pipeline Execution Steps

Run the pipeline steps sequentially to clean datasets, generate the training matrix, train models, tune hyperparameters, and launch the web app.

### 1. Data Cleaning
Normalizes spaces, converts text to lowercase, and standardizes "No Limit" fields.
```bash
python data_cleaning.py
```

### 2. Eligibility Mapping (Training Set Generation)
Runs the Cartesian cross-matching rules between 1,500 users and 100 schemes.
```bash
python create_training_dataset.py
```

### 3. Feature Engineering
Fits and serializes categorical label encoders and saves preprocessed columns.
```bash
python feature_engineering.py
```

### 4. Base Model Training
Trains the Random Forest model with 200 estimators.
```bash
python train_random_forest.py
```

### 5. Hyperparameter Tuning
Performs cross-validated grid search to find the optimal forest depth and split criteria.
```bash
python hyperparameter_tuning.py
```

### 6. Evaluation & Graph Compilation
Generates evaluation figures (ROC Curve, Confusion Matrix, Feature Importance) and writes results to the `graphs/` folder.
```bash
python evaluate_model.py
```

### 7. CLI Inference (Optional)
Run standard terminal queries to test predictions directly in the console.
```bash
python predict.py
```

### 8. Start Web App
Starts the Flask server to launch the GUI dashboard.
```bash
python app.py
```
Open your browser and navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

## Screen Preview

Below is a placeholder indicating where your web interface screen captures will appear:

```text
[Insert Screenshot of User Inputs Form Here]
[Insert Screenshot of Recommendation Cards and Relevance Score Progress Bars Here]
```

---

## Model Evaluation Insights

- **Accuracy & F1 Score**: Since a single user profile may qualify for 10+ different schemes, a user has multiple valid targets in the eligibility map. When evaluated as a single-label multi-class problem, the base model accuracy is naturally low. The recommendation engine instead uses class probabilities (`predict_proba`) and generates a **Top-5 Recommendation list** from the five approved ML inputs.
- **Top Feature Importances**: This model is trained using only the following user attributes: `Age`, `Income`, `Occupation`, `Gender`, and `Category`. These are the only input features passed into the Random Forest pipeline.

---

## Advantages & Limitations

### Advantages
- **Dual Engine Architecture**: Combines exact rule filtration checks with predictive ML probabilities.
- **Explainable Results**: Highlighting required documents and specific benefits helps citizens act immediately.
- **Ultra Responsive UI**: Fluid animations and glassmorphism styling create an premium user experience.

### Limitations
- **Single-Label Multi-Class Modeling**: Traditional Random Forest doesn't represent simultaneous multi-label target classes out-of-the-box, resulting in lower single-prediction metrics. Future iterations could benefit from classifier chains or neural collaborative filtering.
- **Cold Start for New Schemes**: Introducing a brand new scheme requires regenerating the eligibility matching matrix and retraining the model.

---

## Future Scope
- **Multi-Label Multi-Class Models**: Transitioning from Random Forest to neural networks with sigmoid output layers for multi-label classification.
- **Chatbot Integration**: Conversational interface using an LLM to collect demographic parameters naturally.
- **Document OCR**: Enabling upload of identity files (like Aadhaar, PAN) to auto-fill the user demographic form.

---

## IEEE Citation Format
If you utilize this project or code for research, please cite as:
```text
[1] A. Bangar, "AI-Based Government Scheme Recommendation System Using Random Forest Machine Learning," in Proceedings of the IEEE International Conference on Agentic Systems and Web Informatics, 2026, pp. 120-128.
```
