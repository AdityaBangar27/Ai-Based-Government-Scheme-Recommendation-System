"""
=============================================================================
SCRIPT 04: FEATURE ENGINEERING & IMPORTANCE ANALYSIS
Government Scheme Recommendation System
=============================================================================
Purpose : Use a trained Random Forest to compute Gini-based feature
          importances, ranked feature contributions, permutation importance,
          and SHAP-style summary (manual). Saves plots and a report.
Output  : outputs/feature_importance.csv
          outputs/16_feature_importance.png
          reports/feature_importance_report.txt
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import json
import warnings
warnings.filterwarnings('ignore')

PLOT_AVAILABLE = True
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_theme(style='whitegrid')
    plt.rcParams.update({'font.size': 11, 'figure.dpi': 120})
except ImportError:
    PLOT_AVAILABLE = False

from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

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

def save_fig(name):
    if PLOT_AVAILABLE:
        path = os.path.join(OUTPUT_DIR, name)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        log(f'  [Saved] {name}')

# ─── Load & prepare data ──────────────────────────────────────────────────────
section('FEATURE ENGINEERING & IMPORTANCE ANALYSIS')

df = pd.read_csv(USERS_CSV)

# Derived features
df['Is_Low_Income'] = (df['Income'] < 300000).astype(int)
df['Is_Youth']      = (df['Age'] <= 25).astype(int)
df['Is_Vulnerable'] = ((df['Rural_Urban'] == 'Rural') & (df['Is_Low_Income'] == 1)).astype(int)
df['Income_Log']    = np.log1p(df['Income'])   # log-transform to reduce skew

CATEGORICAL_COLS = ['Gender', 'State', 'Education', 'Occupation',
                    'Category', 'Disability_Status', 'Rural_Urban', 'Employment_Status']

encoders = {}
for col in CATEGORICAL_COLS:
    le = LabelEncoder()
    df[col + '_enc'] = le.fit_transform(df[col].astype(str))
    encoders[col] = le

le_y = LabelEncoder()
y = le_y.fit_transform(df['Recommended_Scheme'])

FEATURE_COLS_V1 = [
    'Age', 'Income',
    'Gender_enc', 'State_enc', 'Education_enc', 'Occupation_enc',
    'Category_enc', 'Disability_Status_enc', 'Rural_Urban_enc', 'Employment_Status_enc'
]

FEATURE_COLS_V2 = FEATURE_COLS_V1 + ['Is_Low_Income', 'Is_Youth', 'Is_Vulnerable', 'Income_Log']

X_v1 = df[FEATURE_COLS_V1]
X_v2 = df[FEATURE_COLS_V2]

X_train_v1, X_test_v1, y_train, y_test = train_test_split(X_v1, y, test_size=0.2, random_state=42, stratify=y)
X_train_v2, X_test_v2, _,      _       = train_test_split(X_v2, y, test_size=0.2, random_state=42, stratify=y)

# ─── Train two RF models (baseline vs with engineered features) ───────────────
section('TRAINING RANDOM FOREST — Baseline vs Engineered Features')

from sklearn.metrics import accuracy_score, f1_score

rf_v1 = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf_v1.fit(X_train_v1, y_train)
acc_v1 = accuracy_score(y_test, rf_v1.predict(X_test_v1))
f1_v1  = f1_score(y_test, rf_v1.predict(X_test_v1), average='weighted', zero_division=0)
log(f'  Baseline RF (10 features)          Accuracy={acc_v1*100:.2f}%  F1={f1_v1*100:.2f}%')

rf_v2 = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
rf_v2.fit(X_train_v2, y_train)
acc_v2 = accuracy_score(y_test, rf_v2.predict(X_test_v2))
f1_v2  = f1_score(y_test, rf_v2.predict(X_test_v2), average='weighted', zero_division=0)
log(f'  Engineered RF (14 features)        Accuracy={acc_v2*100:.2f}%  F1={f1_v2*100:.2f}%')

delta_acc = (acc_v2 - acc_v1) * 100
delta_f1  = (f1_v2  - f1_v1)  * 100
log(f'\n  Improvement from feature engineering: Accuracy +{delta_acc:.2f}%  F1 +{delta_f1:.2f}%')

# ─── Gini Importance ─────────────────────────────────────────────────────────
section('GINI-BASED FEATURE IMPORTANCE (Engineered RF)')

importances = rf_v2.feature_importances_
fi_df = pd.DataFrame({
    'Feature': FEATURE_COLS_V2,
    'Importance': importances
}).sort_values('Importance', ascending=False).reset_index(drop=True)
fi_df['Importance_Pct'] = (fi_df['Importance'] * 100).round(2)
fi_df['Rank'] = fi_df.index + 1

log('\n  Rank  Feature                          Importance%   Bar')
log('  ' + '-' * 65)
for _, row in fi_df.iterrows():
    bar = '█' * int(row['Importance_Pct'] * 2)
    log(f"  {int(row['Rank']):>4}  {row['Feature']:<32}  {row['Importance_Pct']:>6.2f}%  {bar}")

fi_df.to_csv(os.path.join(OUTPUT_DIR, 'feature_importance.csv'), index=False)

if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = ['#0ea5e9' if i < 3 else '#6366f1' if i < 6 else '#94a3b8' for i in range(len(fi_df))]
    bars = ax.barh(fi_df['Feature'][::-1], fi_df['Importance_Pct'][::-1], color=colors[::-1])
    ax.set_xlabel('Feature Importance (%)')
    ax.set_title('Random Forest — Feature Importance (Gini Impurity)', fontsize=14, fontweight='bold')
    for bar, val in zip(bars, fi_df['Importance_Pct'][::-1]):
        ax.text(val + 0.2, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}%', va='center', fontsize=9)
    # Legend
    import matplotlib.patches as mpatches
    patches = [
        mpatches.Patch(color='#0ea5e9', label='Top 3 — Critical'),
        mpatches.Patch(color='#6366f1', label='Top 4-6 — High Impact'),
        mpatches.Patch(color='#94a3b8', label='Remaining — Moderate')
    ]
    ax.legend(handles=patches, loc='lower right')
    plt.tight_layout()
    save_fig('16_feature_importance_bar.png')

# ─── Permutation Importance ──────────────────────────────────────────────────
section('PERMUTATION IMPORTANCE (Validation Set)')
log('  Computing... (this may take ~30 seconds)')

perm = permutation_importance(rf_v2, X_test_v2, y_test,
                               n_repeats=5, random_state=42, n_jobs=-1)
perm_df = pd.DataFrame({
    'Feature': FEATURE_COLS_V2,
    'Mean_Decrease': perm.importances_mean,
    'Std': perm.importances_std
}).sort_values('Mean_Decrease', ascending=False).reset_index(drop=True)

log('\n  Rank  Feature                          Mean Accuracy Drop   Std')
log('  ' + '-' * 65)
for i, row in perm_df.iterrows():
    log(f"  {i+1:>4}  {row['Feature']:<32}  {row['Mean_Decrease']:>8.4f}              ±{row['Std']:.4f}")

perm_df.to_csv(os.path.join(OUTPUT_DIR, 'permutation_importance.csv'), index=False)

if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(perm_df['Feature'][::-1], perm_df['Mean_Decrease'][::-1],
            xerr=perm_df['Std'][::-1], color='#f59e0b', alpha=0.8,
            error_kw=dict(elinewidth=1.5, ecolor='#b45309'))
    ax.set_xlabel('Mean Accuracy Decrease')
    ax.set_title('Permutation Importance (Mean ± Std)', fontsize=14, fontweight='bold')
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.tight_layout()
    save_fig('17_permutation_importance.png')

# ─── Feature Correlation with Target ─────────────────────────────────────────
section('FEATURE–TARGET CORRELATION (Point Biserial / Eta)')
X_corr = X_v1.copy()
X_corr['target'] = y
corr_with_target = X_corr.corr()['target'].drop('target').abs().sort_values(ascending=False)
log('\n  Feature                          |Correlation with Target|')
log('  ' + '-' * 55)
for feat, corr in corr_with_target.items():
    bar = '█' * int(corr * 30)
    log(f'  {feat:<32}  {corr:.4f}   {bar}')

# ─── Save report ──────────────────────────────────────────────────────────────
report_path = os.path.join(REPORT_DIR, 'feature_importance_report.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

section('DONE')
log(f'  Outputs: outputs/feature_importance.csv, permutation_importance.csv')
log(f'  Plots  : outputs/16_feature_importance_bar.png, 17_permutation_importance.png')
log(f'  Report : {report_path}')

