# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from bidi.algorithm import get_display
import arabic_reshaper

# Configure matplotlib for Hebrew (right-to-left) text
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display

# Helper function to fix Hebrew text for matplotlib
def fix_hebrew_text(text):
    """Convert Hebrew text to display correctly in matplotlib"""
    if pd.isna(text):
        return text
    reshaped_text = arabic_reshaper.reshape(str(text))
    bidi_text = get_display(reshaped_text)
    return bidi_text

# Paths
EXCEL_PATH = os.path.join(os.path.dirname(__file__), 'data', 'p_libud_23.xlsx')
PLOTS_DIR = os.path.join(os. path.dirname(__file__), 'plots')
os.makedirs(PLOTS_DIR, exist_ok=True)

# Read the third sheet (index 2)
df = pd.read_excel(EXCEL_PATH, sheet_name=2, header=3)

# Select rows 9-265 (Excel is 1-based, pandas is 0-based, so rows 8-264)
df = df.iloc[8:264]

# Rename columns for convenience
df = df.rename(columns={
    df.columns[0]: 'name',
    df.columns[1]: 'id',
    df.columns[2]: 'district',
    df.columns[3]: 'municipal_status',
    df.columns[4]: 'population',
    df.columns[5]: 'socio_economic_index'
})

# Only keep relevant columns
df = df[['name', 'id', 'district', 'municipal_status', 'population', 'socio_economic_index']]

# Drop rows with missing district or municipal_status
df = df. dropna(subset=['district', 'municipal_status'])

# Convert population and socio_economic_index to numeric
df['population'] = pd.to_numeric(df['population'], errors='coerce')
df['socio_economic_index'] = pd.to_numeric(df['socio_economic_index'], errors='coerce')

# Filter categories with <5 authorities for district and municipal_status
district_counts = df['district'].value_counts()
district_to_keep = district_counts[district_counts >= 5].index
district_omit = district_counts[district_counts < 5].index
municipal_counts = df['municipal_status'].value_counts()
municipal_to_keep = municipal_counts[municipal_counts >= 5].index
municipal_omit = municipal_counts[municipal_counts < 5].index

# Omitted authorities (BEFORE filtering)
omitted_districts = df[df['district'].isin(district_omit)][['name', 'district']]
omitted_municipals = df[df['municipal_status'].isin(municipal_omit)][['name', 'municipal_status']]

# Print omitted categories and authorities
if len(district_omit) > 0:
    print('Omitted districts (fewer than 5 authorities):')
    for d in district_omit:
        names = omitted_districts[omitted_districts['district'] == d]['name'].tolist()
        print(f'  {d}: {names}')
if len(municipal_omit) > 0:
    print('Omitted municipal statuses (fewer than 5 authorities):')
    for m in municipal_omit:
        names = omitted_municipals[omitted_municipals['municipal_status'] == m]['name'].tolist()
        print(f'  {m}: {names}')

# Filter main dataframe
df = df[df['district'].isin(district_to_keep)]
df = df[df['municipal_status'].isin(municipal_to_keep)]

# --- IMAGE 1: Bar chart of districts (column C) ---
district_counts_filtered = df['district'].value_counts()
# Fix Hebrew labels
fixed_labels = [fix_hebrew_text(label) for label in district_counts_filtered.index]
plt.figure(figsize=(10,6))
bars = plt.bar(range(len(district_counts_filtered)), district_counts_filtered.values, color='skyblue')
# Add data labels on bars
for i, (bar, value) in enumerate(zip(bars, district_counts_filtered.values)):
    plt.text(bar. get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             str(int(value)), ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.xticks(range(len(district_counts_filtered)), fixed_labels, rotation=45, ha='right')
plt.title(fix_hebrew_text('מחוז (District) - מספר רשויות מקומיות'), fontsize=14)
plt.xlabel(fix_hebrew_text('מחוז (District)'), fontsize=12)
plt.ylabel('Number of Local Authorities', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'districts_bar_chart.png'), format='png', dpi=300, bbox_inches='tight')
plt.close()

# --- IMAGE 2: Side by side pie charts ---
municipal_counts_filtered = df['municipal_status'].value_counts()
pop_by_status = df.groupby('municipal_status')['population'].sum()

# Ensure both use the same category order
categories = municipal_counts_filtered.index
pop_by_status = pop_by_status.reindex(categories)

# Fix Hebrew labels
fixed_labels = [fix_hebrew_text(label) for label in categories]

# Define consistent colors for each category
colors = plt.cm.tab10(range(len(categories)))

# Custom autopct function to show both count/value and percentage
def make_autopct_count(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f'{val}\n({pct:.1f}%)'
    return my_autopct

def make_autopct_pop(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        # Format large numbers with commas
        return f'{val:,}\n({pct:.1f}%)'
    return my_autopct

fig, axes = plt.subplots(1, 2, figsize=(16,8))

# Left pie chart - number of authorities
axes[0].pie(municipal_counts_filtered.values, labels=fixed_labels, 
            autopct=make_autopct_count(municipal_counts_filtered.values), 
            startangle=90, textprops={'fontsize': 10}, colors=colors)
axes[0].set_title(fix_hebrew_text('מעמד מוניציפלי - מספר רשויות'), fontsize=14, pad=20)

# Right pie chart - population
axes[1].pie(pop_by_status.values, labels=fixed_labels, 
            autopct=make_autopct_pop(pop_by_status.values), 
            startangle=90, textprops={'fontsize': 10}, colors=colors)
axes[1].set_title(fix_hebrew_text('מעמד מוניציפלי - סה"כ אוכלוסייה'), fontsize=14, pad=20)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'municipal_status_pie_charts_side_by_side.png'), 
            format='png', dpi=300, bbox_inches='tight')
plt.close()

# --- IMAGE 3: Boxplot for socio-economic index by district (C+F) ---
plt.figure(figsize=(12,8))
data_to_plot = [df[df['district'] == d]['socio_economic_index'].dropna() for d in district_to_keep]
# Fix Hebrew labels
fixed_district_labels = [fix_hebrew_text(label) for label in district_to_keep]

bp = plt.boxplot(data_to_plot, labels=fixed_district_labels, patch_artist=True)

# Color the boxes
for patch in bp['boxes']:
    patch. set_facecolor('lightblue')

# Add median value labels
medians = [np.median(data) for data in data_to_plot]
for i, (median, x_pos) in enumerate(zip(medians, range(1, len(medians) + 1))):
    plt.text(x_pos, median, f'{median:.1f}', 
             ha='center', va='bottom', fontsize=9, fontweight='bold', 
             bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

plt.title(fix_hebrew_text('מדד חברתי כלכלי לפי מחוז (Socio-Economic Index by District)'), fontsize=14)
plt.xlabel(fix_hebrew_text('מחוז (District)'), fontsize=12)
plt.ylabel(fix_hebrew_text('אשכול מדד חברתי כלכלי (Socio-Economic Index)'), fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'socio_economic_index_boxplot.png'), 
            format='png', dpi=300, bbox_inches='tight')
plt.close()

print("All 3 plots saved successfully!")
print(f"  1. districts_bar_chart.png")
print(f"  2. municipal_status_pie_charts_side_by_side.png")
print(f"  3. socio_economic_index_boxplot.png")