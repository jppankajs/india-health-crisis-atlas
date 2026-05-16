import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Base directory of this script (used for all file paths)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets', 'charts')

# page configuration - must be first streamlit command
st.set_page_config(
    page_title="India Health Crisis Atlas",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# load data
@st.cache_data
def load_data():
    data_path = os.path.join(BASE_DIR, '..', 'data', 'processed', 'nfhs5_with_risk_scores.csv')
    df = pd.read_csv(data_path)
    return df

df = load_data()


#sidebar filters

# Sidebar
st.sidebar.markdown("## 🏥 India Health Crisis Atlas")
st.sidebar.markdown("---")
st.sidebar.title("🔍 Filters")


# state filter
all_states = ['All States'] + sorted(df['state'].unique().tolist())
selected_state = st.sidebar.selectbox("Select State", all_states)

# risk category filter
all_risks = ['All Categories', 'Critical Risk', 'High Risk', 'Moderate Risk', 'Low Risk']
selected_risk = st.sidebar.multiselect(
    "Select Risk Category",
    options=['Critical Risk', 'High Risk', 'Moderate Risk', 'Low Risk'],
    default=['Critical Risk', 'High Risk', 'Moderate Risk', 'Low Risk']
)

# apply filters
filtered_df = df.copy()
if selected_state != 'All States':
    filtered_df = filtered_df[filtered_df['state'] == selected_state]
if selected_risk:
    filtered_df = filtered_df[filtered_df['risk_category'].isin(selected_risk)]

st.sidebar.markdown("---")
st.sidebar.metric("Districts shown", len(filtered_df))
st.sidebar.metric("States covered", filtered_df['state'].nunique())

#main dashboard header + kpi cards 

# Main header
st.title("🏥 India Health Crisis Atlas")
st.markdown("**Analyzing health indicators across 707 districts | NFHS-5 (2019-21)**")
st.markdown("---")

# KPI Cards - 4 columns

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_stunting = filtered_df['stunting_pct'].mean()
    st.metric(
        label="Avg Child Stunting",
        value=f"{avg_stunting:.1f}%",
        delta=None if selected_state == 'All States' else f"{avg_stunting - df['stunting_pct'].mean():.1f}% vs national avg"
    )

with col2:
    avg_anaemia = filtered_df['child_anaemia_pct'].mean()
    st.metric(
        label="Avg Child Anaemia",
        value=f"{avg_anaemia:.1f}%",
        delta=None if selected_state == 'All States' else f"{avg_anaemia - df['child_anaemia_pct'].mean():.1f}% vs national avg"
    )

with col3:
    avg_sanitation = filtered_df['sanitation_pct'].mean()
    st.metric(
        label="Avg Sanitation Coverage",
        value=f"{avg_sanitation:.1f}%",
        delta=None if selected_state == 'All States' else f"{avg_sanitation - df['sanitation_pct'].mean():.1f}% vs national avg"
    )

with col4:
    avg_literacy = filtered_df['women_literacy_pct'].mean()
    st.metric(
        label="Avg Women Literacy",
        value=f"{avg_literacy:.1f}%",
        delta=None if selected_state == 'All States' else f"{avg_literacy - df['women_literacy_pct'].mean():.1f}% vs national avg"
    )

st.markdown("---")

# charts sections

# Charts section
st.subheader("📊 Health Indicators Analysis")

col_left, col_right = st.columns(2)

with col_left:
    # Risk category distribution
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    risk_counts = filtered_df['risk_category'].value_counts()
    colors = {
        'Critical Risk': '#d73027',
        'High Risk': '#fc8d59',
        'Moderate Risk': '#fee090',
        'Low Risk': '#91cf60'
    }
    bar_colors = [colors.get(r, 'gray') for r in risk_counts.index]
    ax1.bar(risk_counts.index, risk_counts.values, color=bar_colors, edgecolor='black', linewidth=0.5)
    ax1.set_title('Districts by Risk Category', fontweight='bold')
    ax1.set_ylabel('Number of Districts')
    ax1.tick_params(axis='x', rotation=15)
    for i, v in enumerate(risk_counts.values):
        ax1.text(i, v + 1, str(v), ha='center', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close()

with col_right:
    # Top 10 worst districts by stunting
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    worst10 = filtered_df.nlargest(10, 'stunting_pct')
    ax2.barh(
        worst10['district'] + ', ' + worst10['state'].str[:2],
        worst10['stunting_pct'],
        color='tomato', edgecolor='black', linewidth=0.5
    )
    ax2.set_title('Top 10 Districts — Highest Stunting', fontweight='bold')
    ax2.set_xlabel('Stunting Rate (%)')
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

st.markdown("---")

# Detailed Analysis Charts from EDA
st.subheader("📈 Detailed Analysis Charts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 15 States by Child Stunting Rate**")
    st.image(os.path.join(ASSETS_DIR, '01_stunting_by_state.png'), use_container_width=True)

with col2:
    st.markdown("**Child vs Women Anaemia — Top 15 States**")
    st.image(os.path.join(ASSETS_DIR, '02_anaemia_comparison.png'), use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Correlation Between Health Indicators**")
    st.image(os.path.join(ASSETS_DIR, '03_correlation_heatmap.png'), use_container_width=True)

with col4:
    st.markdown("**District-Level Stunting: Best vs Worst**")
    st.image(os.path.join(ASSETS_DIR, '04_best_worst_districts.png'), use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("**Sanitation vs Child Stunting (Color = Women Literacy)**")
    st.image(os.path.join(ASSETS_DIR, '05_sanitation_vs_stunting.png'), use_container_width=True)

with col6:
    st.markdown("**Optimal Clusters — Elbow & Silhouette Analysis**")
    st.image(os.path.join(ASSETS_DIR, '06_optimal_clusters.png'), use_container_width=True)

st.markdown("---")


# map + data table 

# Interactive Map Section
st.subheader("🗺️ Interactive Health Risk Map")
st.markdown("Click any district dot to see detailed health indicators")

# Embed the folium map
from streamlit.components.v1 import html
with open(os.path.join(BASE_DIR, 'india_health_map.html'), 'r', encoding='utf-8') as f:
    map_html = f.read()

html(map_html, height=500)

st.markdown("---")

# Data Table Section
st.subheader("📋 District-Level Data")

# Column selector
available_cols = ['district', 'state', 'risk_category', 'health_risk_score',
                  'stunting_pct', 'wasting_pct', 'underweight_pct',
                  'child_anaemia_pct', 'women_anaemia_pct',
                  'sanitation_pct', 'clean_water_pct', 'electricity_pct',
                  'women_literacy_pct', 'child_marriage_pct',
                  'institutional_births_pct']

selected_cols = st.multiselect(
    "Select columns to display",
    options=available_cols,
    default=['district', 'state', 'risk_category',
             'health_risk_score', 'stunting_pct', 'child_anaemia_pct']
)

if selected_cols:
    st.dataframe(
        filtered_df[selected_cols].sort_values('health_risk_score', ascending=False),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = filtered_df[selected_cols].to_csv(index=False)
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv,
        file_name='india_health_filtered.csv',
        mime='text/csv'
    )

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
Built by Pankaj | Data: NFHS-5 (2019-21), Government of India |
707 Districts | 101 Health Indicators
</div>
""", unsafe_allow_html=True)

