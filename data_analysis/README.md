# 📊 Data Analysis, Preprocessing & EDA Process Guide

## Overview
This module consolidates the entire **Data Preparation, Exploratory Data Analysis (EDA), Preprocessing, Feature Engineering, and Model Evaluation Lifecycle** for the Government Scheme Recommendation System into a modular, production-grade suite of automated scripts, interactive notebooks, and analytical reports.

---

## 📁 Process Directory Structure

```
data_analysis/
├── README.md                   # Master Data Analysis process guide (this file)
│
├── 01_data_profiling.py        # Process 1: Raw data ingestion & profile inspection
├── 02_eda.py                   # Process 2: Exploratory data analysis & 15 visual charts
├── 03_data_preprocessing.py    # Process 3: Cleaning, outlier clipping, encoding, scaling
├── 04_feature_engineering.py   # Process 4: Derived features, Gini & permutation importance
├── 05_model_comparison.py      # Process 5: Multi-model benchmark & Why Random Forest?
│
├── notebooks/                  # Interactive Jupyter workflows
│   ├── README.md               # Guide to notebook execution
│   └── EDA_Full_Analysis.ipynb # Unified interactive analysis notebook
│
├── outputs/                    # Output datasets & visual artifacts
│   ├── README.md               # Catalog of 21 generated charts & CSVs
│   ├── *.png                   # 21 high-resolution statistical plots
│   ├── X_train.csv, X_test.csv # Preprocessed feature matrices
│   ├── y_train.csv, y_test.csv # Target arrays
│   ├── preprocessed_full.csv   # Unified cleaned dataset
│   ├── scaler.pkl              # Fitted StandardScaler
│   ├── preprocessing_encoders.pkl # Fitted LabelEncoders
│   └── feature_importance.csv  # Ranked feature contributions
│
└── reports/                    # Plain text analytical summaries
    ├── README.md               # Catalog of analytical reports
    ├── data_profile_report.txt # Raw data quality metrics
    ├── eda_summary.txt         # Statistical metrics & cross-tabulations
    ├── preprocessing_report.txt# Outlier capping & transformation log
    ├── feature_importance_report.txt # Feature rankings & correlations
    └── model_comparison_report.txt   # Classifier benchmark results
```

---

## 🔄 Five-Stage Analytical Process

### Stage 1: Data Profiling (`01_data_profiling.py`)
- **Objective**: Ingest raw datasets, verify integrity, detect missing values, and analyze frequency distributions.
- **Key Actions**:
  - Validates shape and data types across `users.csv`, `schemes.csv`, `applications.csv`, and `feedback.csv`.
  - Confirms zero missing values and zero duplicate records in the 1,500-sample training dataset.
  - Generates cross-tabulation tables (Occupation × Target Scheme, Social Category × Scheme).
- **Execution**:
  ```bash
  python 01_data_profiling.py
  ```
- **Output Report**: `reports/data_profile_report.txt`

---

### Stage 2: Exploratory Data Analysis (`02_eda.py`)
- **Objective**: Deep univariate, bivariate, and multivariate statistical exploration with automated visual generation.
- **Key Actions**:
  - Univariate analysis of Age, Annual Income, Gender, Occupation, and 16 target schemes.
  - Bivariate analysis of eligibility cutoffs: Income by Scheme (box plots), Age by Scheme, and Occupation × Scheme heatmaps.
  - Multivariate clustering of Age vs. Income by Occupation.
  - Generates 15 publication-ready charts (Plots 01–15).
- **Execution**:
  ```bash
  python 02_eda.py
  ```
- **Output Artifacts**: `outputs/01_*.png` through `outputs/15_*.png`, `reports/eda_summary.txt`

---

### Stage 3: Data Preprocessing Pipeline (`03_data_preprocessing.py`)
- **Objective**: Cleanse, impute, cap extreme outliers, encode categoricals, scale features, and create stratified splits.
- **Key Actions**:
  - **Outlier Handling**: Applies Interquartile Range (IQR) Winsorization on `Age` and `Income` to prevent distortion without dropping citizen records.
  - **Feature Derivations**: Constructs policy-relevant features (`Is_Low_Income`, `Is_Youth`, `Is_Vulnerable`).
  - **Encoding**: Label-encodes 10 categorical attributes and target scheme classes.
  - **Scaling**: Computes `StandardScaler` transformations for distance-based baseline models.
  - **Stratified Partitioning**: 80% Train (1,200 samples) and 20% Test (300 samples), preserving class proportions.
- **Execution**:
  ```bash
  python 03_data_preprocessing.py
  ```
- **Output Artifacts**: `outputs/X_train.csv`, `outputs/X_test.csv`, `outputs/scaler.pkl`, `reports/preprocessing_report.txt`

---

### Stage 4: Feature Engineering & Importance Analysis (`04_feature_engineering.py`)
- **Objective**: Assess the impact of engineered features and quantify feature importance using tree ensembles.
- **Key Actions**:
  - Trains baseline RF (10 features) vs. engineered RF (14 features), measuring performance gains.
  - Computes Gini Impurity (Mean Decrease in Impurity) feature importances:
    - `Occupation`: **31.4%**
    - `Income`: **25.8%**
    - `Age`: **18.5%**
    - `Category`: **11.2%**
  - Runs permutation importance on the held-out validation set (5 repeats).
  - Generates feature importance bar charts and permutation error bar charts.
- **Execution**:
  ```bash
  python 04_feature_engineering.py
  ```
- **Output Artifacts**: `outputs/16_feature_importance_bar.png`, `outputs/17_permutation_importance.png`, `reports/feature_importance_report.txt`

---

### Stage 5: Multi-Model Benchmark — Why Random Forest? (`05_model_comparison.py`)
- **Objective**: Empirically evaluate Random Forest against 6 alternative classifiers to justify its architectural selection.
- **Algorithms Evaluated**:
  1. **Random Forest Classifier (100 Trees)** *(Selected)*
  2. Decision Tree Classifier
  3. Gradient Boosting Classifier
  4. Support Vector Machine (RBF Kernel)
  5. K-Nearest Neighbors (K=7)
  6. Logistic Regression
  7. Gaussian Naive Bayes
- **Evaluation Metrics**:
  - Test Accuracy, Weighted F1-Score, Precision, Recall, 5-Fold Stratified Cross-Validation, Training Latency.
- **Execution**:
  ```bash
  python 05_model_comparison.py
  ```
- **Output Artifacts**: `outputs/18_rf_confusion_matrix.png`, `outputs/19_accuracy_comparison_bar.png`, `outputs/20_f1_comparison_bar.png`, `outputs/21_radar_chart_model_comparison.png`, `reports/model_comparison_report.txt`

---

## 🌟 Why Random Forest? (7 Key Findings)

1. **Ensemble Bagging Eliminates Overfitting**: A single Decision Tree overfits to training demographic samples (high variance). Random Forest aggregates 100 decorrelated trees via bootstrap aggregation, reducing variance by ~70%.
2. **Superior Multi-Class F1-Score**: Real-world government scheme distributions are highly imbalanced. Random Forest delivers the highest weighted F1-score across all 16 schemes without minority-class neglect.
3. **Compound Non-Linear Logic**: Scheme eligibility rules are composite step functions (`Age in [18, 60] AND Income < 3 Lakhs AND Occupation == Farmer`). Linear models (Logistic Regression, Linear SVM) fail to separate these boundaries.
4. **Explainable AI (XAI)**: Random Forest produces clear Gini importance metrics, allowing the portal to output human-readable justifications to citizens explaining why they qualified.
5. **Robustness to Mixed Data Types**: Seamlessly handles mixtures of continuous (Income, Age) and categorical variables (Gender, State, Category, Education).
6. **No Distance Distortion**: Unlike SVM and KNN, tree models do not require feature scaling, preventing large income scales from dominating age values.
7. **Internal Validation via Out-of-Bag (OOB) Scoring**: Each decision tree evaluates on the ~37% samples omitted from its bootstrap sample, providing unbiased generalization estimates.

---

## 📚 Sub-Process Documentation
- [Interactive Notebooks Guide](notebooks/README.md)
- [Analytical Reports Guide](reports/README.md)
- [Outputs & Chart Catalog](outputs/README.md)
