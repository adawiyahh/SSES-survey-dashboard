import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ======================================
# PAGE HEADER
# ======================================
st.title("🧠 Emotional Resilience Analysis")

# ======================================
# PROBLEM STATEMENT
# ======================================
with st.container():
    st.markdown("### 📝 Problem Statement")
    st.info("""
    Emotional resilience is a key factor in personal and professional success. 
    Understanding how individuals manage stress, adapt to change, control emotions, 
    and maintain motivation can help identify areas for personal development. 
    
    This analysis investigates the relationship between emotional resilience and key 
    personal development attributes such as **adaptability, motivation, emotional control, 
    task persistence, and teamwork skills**. Insights from this study aim to inform 
    strategies for enhancing resilience among participants.
    """)
# ======================================
# OBJECTIVE
# ======================================
    st.markdown("### 🎯 Objective")
    st.write("""
    To investigate the relationship between emotional resilience and personal development 
    attributes, including motivation, adaptability, emotional control, task persistence, 
    and teamwork skills.
    """)

st.markdown("""
Investigating the relationship between emotional resilience and personal development attributes 
including **adaptability, motivation, and teamwork**.
""")

# ======================================
# DATA LOADING 
# ======================================
# This URL points directly to the CSV content
DATA_URL = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/main/dataset/Hafizah_SSES_Cleaned.csv"

@st.cache_data(ttl=3600)  # Cache for 1 hour to improve performance
def load_emotion_data():
    try:
        # User-Agent header helps bypass some security blocks from GitHub
        data = pd.read_csv(DATA_URL, storage_options={'User-Agent': 'Mozilla/5.0'})
        return data
    except Exception as e:
        # If the URL fails, we show a clean error message
        st.error(f"⚠️ Could not connect to the dataset. Please check your internet or the GitHub link.")
        st.exception(e) # This will show the specific error in a collapsed box
        return None

df = load_emotion_data()

# ======================================
# ANALYSIS LOGIC
# ======================================
if df is not None:
    # 1. Define and Clean the Columns
    objective3_cols = [
        'calm_under_pressure', 
        'emotional_control', 
        'adaptability', 
        'self_motivation', 
        'task_persistence', 
        'teamwork'
    ]

    # Verify which columns actually exist in the file
    available_cols = [c for c in objective3_cols if c in df.columns]

    if not available_cols:
        st.error("❌ The required columns were not found in this CSV. Please check the column headers in your file.")
        st.write("Available columns in your file:", df.columns.tolist())
    else:
        # Convert to numeric and fill missing values with median
        df[available_cols] = df[available_cols].apply(pd.to_numeric, errors="coerce")
        df[available_cols] = df[available_cols].fillna(df[available_cols].median())

        # 2. KEY METRICS
        st.subheader("📊 Executive Summary")
        agree_prop = df[available_cols].isin([4, 5]).mean()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Overall Agreement", f"{agree_prop.mean():.1%}")
        m2.metric("Top Strength", agree_prop.idxmax().replace('_', ' ').title())
        m3.metric("Growth Area", agree_prop.idxmin().replace('_', ' ').title())

        # 3. RADAR CHART
        st.subheader("🕸️ Average Resilience Profile")
        mean_scores = df[available_cols].mean()
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=mean_scores.values.tolist() + [mean_scores.values[0]],
            theta=[c.replace('_', ' ').title() for c in available_cols] + [available_cols[0].replace('_', ' ').title()],
            fill='toself',
            fillcolor='rgba(31, 119, 180, 0.5)',
            line_color='#1f77b4'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=False,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # 4. CORRELATION ANALYSIS
        st.subheader("🔗 How Attributes Connect")
        st.write("A higher value (red) means those two strengths often appear together in respondents.")
        corr = df[available_cols].corr()
        fig_corr = px.imshow(
            corr, 
            text_auto=".2f", 
            color_continuous_scale="RdBu_r",
            height=600,
            width=800
        )
        st.plotly_chart(fig_corr, use_container_width=True)

else:
    st.warning("Please verify that the GitHub repository 'SSES-survey-dashboard' is set to **Public**.")
