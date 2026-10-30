# 📓 Interactive Analysis Notebooks Guide

## Overview
This folder contains interactive **Jupyter Notebooks** designed for data scientists, evaluators, and stakeholders wishing to run exploratory analysis, visualize demographic distributions, and train recommendation models in a step-by-step interactive environment.

---

## 📗 Notebook Catalog

### `EDA_Full_Analysis.ipynb`
A complete, self-contained interactive notebook covering all 7 stages of data exploration and modeling:

1. **Dataset Overview**:
   - Automated path resolution and dataset loading (`users.csv`, `schemes.csv`).
   - Schema validation, data types, missing value checks, and summary statistics.
2. **Univariate Analysis**:
   - Histograms and boxplots for Age and Annual Income.
   - Frequency distribution of all 16 target scheme categories.
   - Categorical feature grids for Gender, Occupation, Category, Education, and State.
3. **Bivariate Analysis**:
   - Cross-tabulated count heatmaps for Occupation × Scheme and Category × Scheme.
   - Income spans and age boundaries mapped against target schemes.
   - Multi-class scatter plots exploring feature clustering.
4. **Data Preprocessing Pipeline**:
   - Cleaning and duplicate removal.
   - IQR outlier capping (Winsorization) to avoid data loss.
   - Feature derivation (`Is_Low_Income`, `Is_Youth`, `Is_Vulnerable`).
   - Categorical label encoding and stratified train/test partitioning.
5. **Feature Engineering**:
   - Income quintile grouping (`Very Low` to `Very High`).
   - Interaction flags for vulnerable demographics.
6. **Feature Importance (Explainability)**:
   - Training a Random Forest classifier (100 estimators).
   - Horizontal feature importance bar chart illustrating decision weights.
7. **Model Comparison — Why Random Forest?**:
   - Benchmark table comparing 6 classifiers:
     - Random Forest, Decision Tree, KNN, SVM, Logistic Regression, Gaussian Naive Bayes.
   - Multi-metric grouped bar chart comparing Accuracy, F1-Score, Precision, and Recall.
   - Concrete reasons explaining why Random Forest is chosen for public welfare scheme recommendations.

---

## 🚀 How to Run the Notebooks

### 1. Install Jupyter / VS Code Extension
```bash
pip install jupyter notebook
```

### 2. Launch Jupyter Notebook Server
```bash
cd data_analysis/notebooks
jupyter notebook
```
Or open `EDA_Full_Analysis.ipynb` directly in VS Code / Cursor with the Python & Jupyter extensions installed.

