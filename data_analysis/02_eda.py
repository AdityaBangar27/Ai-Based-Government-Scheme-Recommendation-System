"""
=============================================================================
SCRIPT 02: EXPLORATORY DATA ANALYSIS (EDA)
Government Scheme Recommendation System
=============================================================================
Purpose : Full EDA — univariate, bivariate, and multivariate analysis with
          matplotlib/seaborn visualizations saved to outputs/.
          Also generates a text summary in reports/eda_summary.txt
Output  : outputs/*.png  +  reports/eda_summary.txt
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ─── Try to import plotting libraries ─────────────────────────────────────────
PLOT_AVAILABLE = True
try:
    import matplotlib
    matplotlib.use('Agg')          # Non-interactive backend (works without display)
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import seaborn as sns
    sns.set_theme(style='whitegrid', palette='Set2')
    plt.rcParams.update({'font.size': 11, 'figure.dpi': 120})
except ImportError:
    PLOT_AVAILABLE = False
    print('[WARN] matplotlib / seaborn not installed. Running text-only EDA.')

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_CSV   = os.path.join(BASE_DIR, 'scheme-recommender', 'users.csv')
SCHEMES_CSV = os.path.join(BASE_DIR, 'datasets', 'schemes.csv')
OUTPUT_DIR  = os.path.join(BASE_DIR, 'data_analysis', 'outputs')
REPORT_DIR  = os.path.join(BASE_DIR, 'data_analysis', 'reports')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

report_lines = []

def log(msg=''):
    print(msg)
    report_lines.append(str(msg))

def save_fig(name):
    if PLOT_AVAILABLE:
        path = os.path.join(OUTPUT_DIR, name)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        log(f'  [Saved] {name}')

# ─── Load data ────────────────────────────────────────────────────────────────
log('=' * 70)
log('  EDA — Government Scheme Recommendation Dataset')
log('=' * 70)

df = pd.read_csv(USERS_CSV)
schemes_df = pd.read_csv(SCHEMES_CSV)

log(f'\n[INFO] Users dataset: {df.shape[0]} rows × {df.shape[1]} columns')
log(f'[INFO] Schemes dataset: {schemes_df.shape[0]} rows × {schemes_df.shape[1]} columns')
log(f'[INFO] Target classes: {df["Recommended_Scheme"].nunique()} unique schemes')

# ═══════════════════════════════════════════════════════════════════════════════
# 1. UNIVARIATE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
log('\n\n── 1. UNIVARIATE ANALYSIS ──────────────────────────────────────────────')

# 1a. Age Distribution
log('\n[1a] Age Distribution')
log(df['Age'].describe().round(2).to_string())

if PLOT_AVAILABLE:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Age Distribution', fontsize=15, fontweight='bold')
    axes[0].hist(df['Age'], bins=20, color='#0ea5e9', edgecolor='white', linewidth=0.5)
    axes[0].set_xlabel('Age'); axes[0].set_ylabel('Count'); axes[0].set_title('Histogram')
    axes[1].boxplot(df['Age'], vert=True, patch_artist=True,
                    boxprops=dict(facecolor='#0ea5e9', color='navy'),
                    medianprops=dict(color='white', linewidth=2))
    axes[1].set_ylabel('Age'); axes[1].set_title('Box Plot')
    plt.tight_layout()
    save_fig('01_age_distribution.png')

# 1b. Income Distribution
log('\n[1b] Income Distribution')
log(df['Income'].describe().round(2).to_string())
log(f'  Skewness: {df["Income"].skew():.4f}')
log(f'  Kurtosis: {df["Income"].kurtosis():.4f}')

if PLOT_AVAILABLE:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Annual Income Distribution', fontsize=15, fontweight='bold')
    axes[0].hist(df['Income'] / 1000, bins=25, color='#10b981', edgecolor='white', linewidth=0.5)
    axes[0].set_xlabel('Income (thousands INR)'); axes[0].set_ylabel('Count')
    axes[0].set_title('Histogram')
    axes[1].boxplot(df['Income'] / 1000, patch_artist=True,
                    boxprops=dict(facecolor='#10b981', color='darkgreen'),
                    medianprops=dict(color='white', linewidth=2))
    axes[1].set_ylabel('Income (thousands INR)'); axes[1].set_title('Box Plot')
    plt.tight_layout()
    save_fig('02_income_distribution.png')

# 1c. Gender Distribution
log('\n[1c] Gender Distribution')
gender_cnt = df['Gender'].value_counts()
for g, c in gender_cnt.items():
    log(f'  {g}: {c} ({c/len(df)*100:.1f}%)')

if PLOT_AVAILABLE:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Gender Distribution', fontsize=15, fontweight='bold')
    colors = ['#3b82f6', '#f472b6']
    axes[0].bar(gender_cnt.index, gender_cnt.values, color=colors, edgecolor='white')
    axes[0].set_title('Bar Chart'); axes[0].set_ylabel('Count')
    axes[1].pie(gender_cnt.values, labels=gender_cnt.index, autopct='%1.1f%%',
                colors=colors, startangle=90)
    axes[1].set_title('Pie Chart')
    plt.tight_layout()
    save_fig('03_gender_distribution.png')

# 1d. Occupation
log('\n[1d] Occupation Distribution')
occ_cnt = df['Occupation'].value_counts()
for o, c in occ_cnt.items():
    log(f'  {o}: {c} ({c/len(df)*100:.1f}%)')

if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(occ_cnt.index, occ_cnt.values,
                   color=['#0ea5e9', '#10b981', '#f59e0b', '#6366f1'])
    ax.set_xlabel('Count'); ax.set_title('Occupation Distribution', fontsize=14, fontweight='bold')
    for bar, val in zip(bars, occ_cnt.values):
        ax.text(val + 5, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=10)
    plt.tight_layout()
    save_fig('04_occupation_distribution.png')

# 1e. Recommended Scheme (Target)
log('\n[1e] Target Variable — Recommended_Scheme')
scheme_cnt = df['Recommended_Scheme'].value_counts()
for s, c in scheme_cnt.items():
    log(f'  {s}: {c} ({c/len(df)*100:.1f}%)')

if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(13, 6))
    palette = plt.cm.tab20.colors[:len(scheme_cnt)]
    bars = ax.barh(scheme_cnt.index, scheme_cnt.values, color=palette)
    ax.set_xlabel('Number of Citizens'); ax.set_title('Distribution of Recommended Schemes (Target Variable)',
                                                         fontsize=13, fontweight='bold')
    for bar, val in zip(bars, scheme_cnt.values):
        ax.text(val + 3, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=9)
    plt.tight_layout()
    save_fig('05_scheme_target_distribution.png')

# 1f. Categorical Columns
for col in ['Category', 'Education', 'State', 'Disability_Status', 'Rural_Urban', 'Employment_Status']:
    log(f'\n[1f] {col}')
    cnt = df[col].value_counts()
    for v, c in cnt.items():
        log(f'  {v}: {c} ({c/len(df)*100:.1f}%)')

if PLOT_AVAILABLE:
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Categorical Feature Distributions', fontsize=15, fontweight='bold')
    cats = ['Category', 'Education', 'State', 'Disability_Status', 'Rural_Urban', 'Employment_Status']
    for ax, col in zip(axes.flatten(), cats):
        cnt = df[col].value_counts()
        ax.bar(cnt.index, cnt.values, color='#6366f1', edgecolor='white')
        ax.set_title(col, fontsize=11, fontweight='bold')
        ax.tick_params(axis='x', rotation=30)
        ax.set_ylabel('Count')
    plt.tight_layout()
    save_fig('06_categorical_distributions.png')

# ═══════════════════════════════════════════════════════════════════════════════
# 2. BIVARIATE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
log('\n\n── 2. BIVARIATE ANALYSIS ──────────────────────────────────────────────')

# 2a. Age vs Income scatter
log('\n[2a] Age vs Income Scatter')
if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(10, 6))
    occ_list = df['Occupation'].unique()
    colors_occ = ['#0ea5e9', '#10b981', '#f59e0b', '#6366f1']
    for occ, col in zip(occ_list, colors_occ):
        subset = df[df['Occupation'] == occ]
        ax.scatter(subset['Age'], subset['Income'] / 1000, alpha=0.5,
                   label=occ, color=col, s=40)
    ax.set_xlabel('Age'); ax.set_ylabel('Income (thousands INR)')
    ax.set_title('Age vs Income by Occupation', fontsize=13, fontweight='bold')
    ax.legend()
    plt.tight_layout()
    save_fig('07_age_vs_income_scatter.png')

# 2b. Income by Recommended Scheme — boxplot
log('\n[2b] Income by Recommended Scheme')
median_income = df.groupby('Recommended_Scheme')['Income'].median().sort_values()
for s, v in median_income.items():
    log(f'  {s}: Median INR {v:,.0f}')

if PLOT_AVAILABLE:
    scheme_order = median_income.index.tolist()
    fig, ax = plt.subplots(figsize=(14, 7))
    df_sorted = df.copy()
    df_sorted['Recommended_Scheme'] = pd.Categorical(df_sorted['Recommended_Scheme'],
                                                      categories=scheme_order, ordered=True)
    groups = [df_sorted[df_sorted['Recommended_Scheme'] == s]['Income'].values / 1000
               for s in scheme_order]
    bp = ax.boxplot(groups, vert=False, patch_artist=True,
               boxprops=dict(facecolor='#e0f2fe', color='#0369a1'),
               medianprops=dict(color='#0369a1', linewidth=2))
    ax.set_yticks(range(1, len(scheme_order) + 1))
    ax.set_yticklabels(scheme_order)
    ax.set_xlabel('Income (thousands INR)')
    ax.set_title('Income Distribution by Recommended Scheme', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_fig('08_income_by_scheme.png')

# 2c. Age by Recommended Scheme
log('\n[2c] Age by Recommended Scheme')
median_age = df.groupby('Recommended_Scheme')['Age'].median().sort_values()
for s, v in median_age.items():
    log(f'  {s}: Median age {v:.1f}')

if PLOT_AVAILABLE:
    scheme_order_age = median_age.index.tolist()
    fig, ax = plt.subplots(figsize=(14, 7))
    groups_age = [df[df['Recommended_Scheme'] == s]['Age'].values for s in scheme_order_age]
    bp2 = ax.boxplot(groups_age, vert=False, patch_artist=True,
               boxprops=dict(facecolor='#dcfce7', color='#166534'),
               medianprops=dict(color='#166534', linewidth=2))
    ax.set_yticks(range(1, len(scheme_order_age) + 1))
    ax.set_yticklabels(scheme_order_age)
    ax.set_xlabel('Age (years)')
    ax.set_title('Age Distribution by Recommended Scheme', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_fig('09_age_by_scheme.png')

# 2d. Occupation vs Scheme — heatmap
log('\n[2d] Occupation vs Scheme Heatmap')
ct = pd.crosstab(df['Occupation'], df['Recommended_Scheme'])
log(ct.to_string())

if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(16, 5))
    sns.heatmap(ct, annot=True, fmt='d', cmap='Blues', linewidths=0.5, ax=ax)
    ax.set_title('Occupation × Recommended Scheme (Count Heatmap)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Recommended Scheme'); ax.set_ylabel('Occupation')
    plt.xticks(rotation=35, ha='right')
    plt.tight_layout()
    save_fig('10_occupation_scheme_heatmap.png')

# 2e. Category vs Scheme
log('\n[2e] Category vs Scheme Heatmap')
ct2 = pd.crosstab(df['Category'], df['Recommended_Scheme'])
if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(16, 5))
    sns.heatmap(ct2, annot=True, fmt='d', cmap='Purples', linewidths=0.5, ax=ax)
    ax.set_title('Social Category × Recommended Scheme (Count Heatmap)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Recommended Scheme'); ax.set_ylabel('Category')
    plt.xticks(rotation=35, ha='right')
    plt.tight_layout()
    save_fig('11_category_scheme_heatmap.png')

# 2f. State vs Scheme
log('\n[2f] State vs Scheme')
ct3 = pd.crosstab(df['State'], df['Recommended_Scheme'])
log(ct3.to_string())

if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(16, 7))
    sns.heatmap(ct3, annot=True, fmt='d', cmap='Oranges', linewidths=0.5, ax=ax)
    ax.set_title('State × Recommended Scheme (Count Heatmap)', fontsize=13, fontweight='bold')
    plt.xticks(rotation=35, ha='right')
    plt.tight_layout()
    save_fig('12_state_scheme_heatmap.png')

# ═══════════════════════════════════════════════════════════════════════════════
# 3. MULTIVARIATE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
log('\n\n── 3. MULTIVARIATE ANALYSIS ───────────────────────────────────────────')

# 3a. Correlation Matrix (numeric only)
log('\n[3a] Numeric Correlation Matrix')
num_df = df[['Age', 'Income']].copy()
corr_matrix = num_df.corr().round(4)
log(corr_matrix.to_string())

if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                linewidths=1, fmt='.4f', ax=ax)
    ax.set_title('Numeric Feature Correlation Matrix', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_fig('13_correlation_matrix.png')

# 3b. Pair plot — Age, Income by Occupation
if PLOT_AVAILABLE:
    fig, ax = plt.subplots(figsize=(10, 6))
    for occ, col in zip(df['Occupation'].unique(), ['#0ea5e9', '#10b981', '#f59e0b', '#6366f1']):
        subset = df[df['Occupation'] == occ]
        ax.scatter(subset['Age'], subset['Income'] / 1000, alpha=0.4,
                   label=occ, color=col, s=50, edgecolors='white', linewidth=0.5)
    ax.set_xlabel('Age'); ax.set_ylabel('Income (K INR)')
    ax.set_title('Age vs Income — Coloured by Occupation', fontsize=13, fontweight='bold')
    ax.legend(title='Occupation')
    plt.tight_layout()
    save_fig('14_multivariate_scatter.png')

# 3c. Disability + Rural/Urban vs Scheme count
log('\n[3c] Disability Status & Rural/Urban vs Schemes')
ct4 = pd.crosstab([df['Disability_Status'], df['Rural_Urban']], df['Recommended_Scheme'])
log(ct4.to_string())

# 3d. Education vs Income violin
if PLOT_AVAILABLE:
    edu_order = ['5th', '10th', '12th', 'Diploma', 'Graduate', 'BTech', 'MBA']
    edu_present = [e for e in edu_order if e in df['Education'].unique()]
    fig, ax = plt.subplots(figsize=(13, 6))
    parts = ax.violinplot([df[df['Education'] == e]['Income'].values / 1000 for e in edu_present],
                           positions=range(len(edu_present)), showmedians=True)
    for pc in parts['bodies']:
        pc.set_facecolor('#6366f1'); pc.set_alpha(0.6)
    ax.set_xticks(range(len(edu_present))); ax.set_xticklabels(edu_present)
    ax.set_xlabel('Education Level'); ax.set_ylabel('Income (thousands INR)')
    ax.set_title('Income Distribution by Education Level (Violin Plot)', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_fig('15_income_by_education_violin.png')

# ─── Save summary report ──────────────────────────────────────────────────────
report_path = os.path.join(REPORT_DIR, 'eda_summary.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

log('\n' + '=' * 70)
log(f'  EDA Complete. Plots saved to: {OUTPUT_DIR}')
log(f'  Summary report: {report_path}')
log('=' * 70)
