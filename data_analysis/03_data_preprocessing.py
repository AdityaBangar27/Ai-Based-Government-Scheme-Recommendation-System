"""
=============================================================================
SCRIPT 03: DATA PREPROCESSING PIPELINE
Government Scheme Recommendation System
=============================================================================
Purpose : Full preprocessing pipeline — cleaning, outlier handling,
          label encoding, normalization, and train/test split.
          Saves preprocessed datasets to outputs/ for use by ML scripts.
Output  : outputs/X_train.csv, X_test.csv, y_train.csv, y_test.csv
          outputs/preprocessed_full.csv
          reports/preprocessing_report.txt
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import json
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_CSV   = os.path.join(BASE_DIR, 'scheme-recommender', 'users.csv')
OUTPUT_DIR  = os.path.join(BASE_DIR, 'data_analysis', 'outputs')
REPORT_DIR  = os.path.join(BASE_DIR, 'data_analysis', 'reports')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

lines = []
def log(msg=''):
    print(msg)
    lines.append(str(msg))

def section(title):
    log('\n' + '=' * 70)
    log(f'  {title}')
    log('=' * 70)

# ─── Load raw data ────────────────────────────────────────────────────────────
section('STEP 1: LOAD RAW DATA')
df_raw = pd.read_csv(USERS_CSV)
log(f'  Loaded: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns')
log(f'  Columns: {list(df_raw.columns)}')

# ─── Step 2: Missing Value Analysis ──────────────────────────────────────────
section('STEP 2: MISSING VALUE ANALYSIS')
missing = df_raw.isnull().sum()
log('\n  Column                               Missing   Pct')
log('  ' + '-' * 50)
for col, n in missing.items():
    pct = n / len(df_raw) * 100
    status = 'OK' if n == 0 else 'IMPUTE'
    log(f'  {col:<35} {n:>5}   {pct:5.1f}%   [{status}]')

# Impute if any missing (none expected in this dataset)
for col in df_raw.select_dtypes(include=[np.number]).columns:
    df_raw[col].fillna(df_raw[col].median(), inplace=True)
for col in df_raw.select_dtypes(include='object').columns:
    df_raw[col].fillna(df_raw[col].mode()[0], inplace=True)
log(f'\n  Missing values after imputation: {df_raw.isnull().sum().sum()}')

# ─── Step 3: Duplicate Detection & Removal ────────────────────────────────────
section('STEP 3: DUPLICATE DETECTION')
dups = df_raw.duplicated().sum()
log(f'  Duplicate rows found: {dups}')
df_clean = df_raw.drop_duplicates().reset_index(drop=True)
log(f'  Dataset after dedup: {df_clean.shape[0]} rows')

# ─── Step 4: Outlier Detection & Capping (IQR) ───────────────────────────────
section('STEP 4: OUTLIER DETECTION & CAPPING (IQR Method)')
df_processed = df_clean.copy()

for col in ['Age', 'Income']:
    Q1 = df_processed[col].quantile(0.25)
    Q3 = df_processed[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df_processed[(df_processed[col] < lower) | (df_processed[col] > upper)].shape[0]
    log(f'\n  [{col}]')
    log(f'    Q1={Q1:.1f}, Q3={Q3:.1f}, IQR={IQR:.1f}')
    log(f'    Lower fence={lower:.1f}, Upper fence={upper:.1f}')
    log(f'    Outliers detected: {outliers}')
    # Cap (Winsorize) — keep but clip to fence values
    df_processed[col] = df_processed[col].clip(lower=lower, upper=upper)
    log(f'    Outliers capped (Winsorized) — no rows dropped.')

# ─── Step 5: Feature Engineering — new derived features ──────────────────────
section('STEP 5: FEATURE ENGINEERING — Derived Features')

# Income group (quintile bucket)
df_processed['Income_Group'] = pd.qcut(
    df_processed['Income'], q=5,
    labels=['Very Low', 'Low', 'Middle', 'High', 'Very High']
).astype(str)
log('  [+] Income_Group — 5-quintile bucket (Very Low → Very High)')

# Age group
bins   = [0, 18, 25, 35, 45, 55, 65, 100]
labels = ['Child', 'Youth', 'Young Adult', 'Adult', 'Middle Age', 'Senior', 'Elderly']
df_processed['Age_Group'] = pd.cut(df_processed['Age'], bins=bins,
                                    labels=labels, right=True).astype(str)
log('  [+] Age_Group — life-stage bucket (Child → Elderly)')

# Is low income flag (below 3 Lakhs annual)
df_processed['Is_Low_Income'] = (df_processed['Income'] < 300000).astype(int)
log('  [+] Is_Low_Income — binary flag for income < ₹3,00,000')

# Is youth flag
df_processed['Is_Youth'] = (df_processed['Age'] <= 25).astype(int)
log('  [+] Is_Youth — binary flag for age ≤ 25')

# Is rural + low income (most vulnerable segment)
df_processed['Is_Vulnerable'] = (
    (df_processed['Rural_Urban'] == 'Rural') & 
    (df_processed['Is_Low_Income'] == 1)
).astype(int)
log('  [+] Is_Vulnerable — Rural AND Low Income binary flag')

log(f'\n  Dataset after feature engineering: {df_processed.shape}')

# ─── Step 6: Encoding ────────────────────────────────────────────────────────
section('STEP 6: LABEL ENCODING — Categorical → Numeric')

TARGET_COL  = 'Recommended_Scheme'
CATEGORICAL_COLS = [
    'Gender', 'State', 'Education', 'Occupation', 'Category',
    'Disability_Status', 'Rural_Urban', 'Employment_Status',
    'Income_Group', 'Age_Group'
]

encoders = {}
df_encoded = df_processed.copy()

for col in CATEGORICAL_COLS:
    le = LabelEncoder()
    df_encoded[col + '_enc'] = le.fit_transform(df_encoded[col].astype(str))
    encoders[col] = le
    log(f'  {col:<25} → {col}_enc   Classes: {list(le.classes_)}')

# Encode target
le_target = LabelEncoder()
df_encoded['Scheme_Label'] = le_target.fit_transform(df_encoded[TARGET_COL])
encoders['target'] = le_target
log(f'\n  Target encoding: {TARGET_COL} → Scheme_Label')
log(f'  Classes ({len(le_target.classes_)}): {list(le_target.classes_)}')

# ─── Step 7: Feature Selection for ML ────────────────────────────────────────
section('STEP 7: FEATURE SELECTION FOR ML')

FEATURE_COLS = [
    'Age', 'Income',
    'Gender_enc', 'State_enc', 'Education_enc', 'Occupation_enc',
    'Category_enc', 'Disability_Status_enc', 'Rural_Urban_enc',
    'Employment_Status_enc',
    'Is_Low_Income', 'Is_Youth', 'Is_Vulnerable'
]

X = df_encoded[FEATURE_COLS].copy()
y = df_encoded['Scheme_Label'].copy()

log(f'  Feature matrix X: {X.shape}')
log(f'  Target vector  y: {y.shape}')
log(f'  Selected features: {FEATURE_COLS}')

# ─── Step 8: Scaling ─────────────────────────────────────────────────────────
section('STEP 8: FEATURE SCALING')
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=FEATURE_COLS)
log('  Applied StandardScaler to all features.')
log('  (Note: Tree-based models like Random Forest do not require scaling,')
log('   but scaled data is provided for SVM / KNN / Logistic Regression benchmarks.)')

# ─── Step 9: Train-Test Split ─────────────────────────────────────────────────
section('STEP 9: TRAIN / TEST SPLIT')
TEST_SIZE   = 0.2
RANDOM_SEED = 42

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
)
X_train_scaled, X_test_scaled, _, _ = train_test_split(
    X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
)

log(f'  Strategy : Stratified split (preserves class proportions)')
log(f'  Test size: {TEST_SIZE * 100:.0f}%')
log(f'  Train set: {X_train_raw.shape[0]} samples')
log(f'  Test set : {X_test_raw.shape[0]} samples')
log(f'\n  Class distribution in train:')
for lbl, cnt in y_train.value_counts().items():
    scheme = le_target.inverse_transform([lbl])[0]
    log(f'    {scheme:<35} {cnt}')

# ─── Step 10: Save outputs ───────────────────────────────────────────────────
section('STEP 10: SAVING OUTPUTS')

X_train_raw.to_csv(os.path.join(OUTPUT_DIR, 'X_train.csv'), index=False)
X_test_raw.to_csv(os.path.join(OUTPUT_DIR, 'X_test.csv'), index=False)
X_train_scaled.to_csv(os.path.join(OUTPUT_DIR, 'X_train_scaled.csv'), index=False)
X_test_scaled.to_csv(os.path.join(OUTPUT_DIR, 'X_test_scaled.csv'), index=False)
y_train.to_csv(os.path.join(OUTPUT_DIR, 'y_train.csv'), index=False)
y_test.to_csv(os.path.join(OUTPUT_DIR, 'y_test.csv'), index=False)
df_encoded.to_csv(os.path.join(OUTPUT_DIR, 'preprocessed_full.csv'), index=False)

# Save encoders & scaler
joblib.dump(encoders, os.path.join(OUTPUT_DIR, 'preprocessing_encoders.pkl'))
joblib.dump(scaler,   os.path.join(OUTPUT_DIR, 'scaler.pkl'))

# Save feature config JSON
config = {
    'feature_columns': FEATURE_COLS,
    'categorical_cols': CATEGORICAL_COLS,
    'target_col': TARGET_COL,
    'scheme_classes': list(le_target.classes_),
    'test_size': TEST_SIZE,
    'random_seed': RANDOM_SEED,
    'n_train': int(X_train_raw.shape[0]),
    'n_test': int(X_test_raw.shape[0])
}
with open(os.path.join(OUTPUT_DIR, 'preprocessing_config.json'), 'w') as f:
    json.dump(config, f, indent=4)

log('  Files saved:')
for fname in ['X_train.csv', 'X_test.csv', 'X_train_scaled.csv', 'X_test_scaled.csv',
              'y_train.csv', 'y_test.csv', 'preprocessed_full.csv',
              'preprocessing_encoders.pkl', 'scaler.pkl', 'preprocessing_config.json']:
    log(f'    outputs/{fname}')

# ─── Save report ──────────────────────────────────────────────────────────────
report_path = os.path.join(REPORT_DIR, 'preprocessing_report.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

section('PREPROCESSING PIPELINE COMPLETE')
log(f'  Report saved: {report_path}')

