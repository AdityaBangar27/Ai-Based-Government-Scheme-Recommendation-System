# 🧪 Scheme Recommender Prototype & Benchmark Dataset

## Overview
This directory preserves the **original research prototype and benchmark training dataset** (1,500 citizen profile records) used to design the machine learning algorithms for the Government Scheme Recommendation System.

---

## 📁 File Manifest

| File | Type | Description |
|---|---|---|
| `users.csv` | Dataset | Benchmark dataset containing 1,500 labeled citizen profiles |
| `schemes.csv` | Dataset | Reference scheme criteria catalog used in initial experimentation |
| `model.py` | Python Script | Original prototype script for training and exporting Random Forest models |
| `encoders.pkl` | Binary Artifact | Serialized LabelEncoders from the prototype stage |
| `scheme_model.pkl` | Binary Artifact | Historical Random Forest model weights (100 estimators) |

---

## 📊 Benchmark Dataset Specification (`users.csv`)
- **Total Records**: 1,500 rows
- **Target Variable**: `Recommended_Scheme` (16 unique government welfare schemes)
- **Features Included**:
  - `Age` (Range: 17 to 65 years)
  - `Gender` (Male, Female)
  - `Income` (Range: ₹5,000 to ₹11,99,383)
  - `State` (8 states: Maharashtra, Karnataka, Bihar, Gujarat, MP, Rajasthan, UP, TN)
  - `Education` (5th, 10th, 12th, Diploma, Graduate, BTech, MBA)
  - `Occupation` (Farmer, Student, Entrepreneur, Artisan)
  - `Category` (General, OBC, SC, ST)
  - `Disability_Status` (Yes, No)
  - `Rural_Urban` (Rural, Urban)
  - `Employment_Status` (Farmer, Student, Entrepreneur, Artisan)

---

## 🔄 Relationship to Active System
The active production microservice resides in `ml_model/` and `server/controllers/recommendationController.js`. The comprehensive data analysis and preprocessing pipeline in `data_analysis/` directly utilizes `users.csv` from this folder as its primary ground-truth dataset.

