"""
=============================================================================
SCRIPT 01: DATA PROFILING
Government Scheme Recommendation System
=============================================================================
Purpose : Inspect the raw datasets — shape, column types, missing values,
          duplicates, value distributions, and data quality summary.
Output  : Console report + reports/data_profile_report.txt
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_CSV   = os.path.join(BASE_DIR, 'scheme-recommender', 'users.csv')
SCHEMES_CSV = os.path.join(BASE_DIR, 'datasets', 'schemes.csv')
APPS_CSV    = os.path.join(BASE_DIR, 'datasets', 'applications.csv')
FEEDBACK_CSV= os.path.join(BASE_DIR, 'datasets', 'feedback.csv')
REPORT_DIR  = os.path.join(BASE_DIR, 'data_analysis', 'reports')
os.makedirs(REPORT_DIR, exist_ok=True)

lines = []

def log(msg=''):
    msg_str = str(msg).encode('ascii', errors='replace').decode('ascii')
    print(msg_str)
    lines.append(str(msg))

def section(title):
    border = '=' * 70
    log(border)
    log(f'  {title}')
    log(border)

def sub(title):
    log(f'\n--- {title} ---')


# ─── Load ─────────────────────────────────────────────────────────────────────
section('DATA PROFILING REPORT')
log(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

datasets = {}
for label, path in [
    ('Users (Training)', USERS_CSV),
    ('Schemes', SCHEMES_CSV),
    ('Applications', APPS_CSV),
    ('Feedback', FEEDBACK_CSV),
]:
    if os.path.exists(path):
        df = pd.read_csv(path)
        datasets[label] = df
        log(f'  [OK] Loaded {label}: {df.shape[0]} rows x {df.shape[1]} cols')
    else:
        log(f'  [SKIP] {label}: file not found at {path}')

# ─── Per-dataset profiling ─────────────────────────────────────────────────────
for name, df in datasets.items():
    section(f'DATASET: {name}')

    sub('Shape')
    log(f'  Rows: {df.shape[0]}   Columns: {df.shape[1]}')

    sub('Columns & Data Types')
    for col in df.columns:
        log(f'  {col:<35} {str(df[col].dtype):<12}')

    sub('Missing Values')
    miss = df.isnull().sum()
    if miss.sum() == 0:
        log('  No missing values detected.')
    else:
        for col, n in miss[miss > 0].items():
            pct = n / len(df) * 100
            log(f'  {col:<35} {n} missing  ({pct:.1f}%)')

    sub('Duplicate Rows')
    dups = df.duplicated().sum()
    log(f'  Duplicate rows: {dups}')

    sub('Numeric Columns — Descriptive Statistics')
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        desc = df[num_cols].describe().round(2)
        log(desc.to_string())
    else:
        log('  No numeric columns.')

    sub('Categorical Columns — Unique Value Counts')
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    for col in cat_cols:
        n_unique = df[col].nunique()
        top = df[col].value_counts().head(5)
        log(f'\n  [{col}]  — {n_unique} unique values')
        for val, cnt in top.items():
            pct = cnt / len(df) * 100
            log(f'    {str(val):<30} {cnt:>5}  ({pct:.1f}%)')

# ─── Users dataset — deeper dive ──────────────────────────────────────────────
if 'Users (Training)' in datasets:
    df = datasets['Users (Training)']
    section('DEEPER DIVE: Users Training Dataset')

    sub('Age Distribution Buckets')
    bins   = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = ['<18', '18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    age_groups = pd.cut(df['Age'], bins=bins, labels=labels, right=True)
    for lbl, cnt in age_groups.value_counts().sort_index().items():
        bar = '█' * (cnt // 20)
        log(f'  {lbl:<8}: {cnt:>4}  {bar}')

    sub('Income Distribution Buckets (INR)')
    inc_bins  = [0, 100000, 300000, 500000, 800000, 1500000]
    inc_lbls  = ['< 1L', '1L-3L', '3L-5L', '5L-8L', '8L+']
    inc_grp   = pd.cut(df['Income'], bins=inc_bins, labels=inc_lbls, right=True)
    for lbl, cnt in inc_grp.value_counts().sort_index().items():
        bar = '█' * (cnt // 25)
        log(f'  {str(lbl):<10}: {cnt:>4}  {bar}')

    sub('Scheme Distribution (Target Variable)')
    for scheme, cnt in df['Recommended_Scheme'].value_counts().items():
        pct = cnt / len(df) * 100
        bar = '█' * int(pct)
        log(f'  {str(scheme):<35} {cnt:>4}  {pct:5.1f}%  {bar}')

    sub('Cross-tab: Occupation vs Recommended_Scheme (top associations)')
    ct = pd.crosstab(df['Occupation'], df['Recommended_Scheme'])
    log(ct.to_string())

    sub('Cross-tab: Category vs Recommended_Scheme')
    ct2 = pd.crosstab(df['Category'], df['Recommended_Scheme'])
    log(ct2.to_string())

# ─── Save report ─────────────────────────────────────────────────────────────
report_path = os.path.join(REPORT_DIR, 'data_profile_report.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

section('DONE')
log(f'  Report saved to: {report_path}')
