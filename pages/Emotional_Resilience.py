import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="Emotional Resilience Analysis",
    layout="wide"
)

st.title("Emotional Resilience and Personal Development")

st.markdown("""
**Objective:**  
To investigate the relationship between emotional resilience and personal development attributes,
including motivation, adaptability, emotional control, task persistence, and teamwork skills.
""")

# ======================================
# LOAD CLEANED DATASET (HAFIZAH VERSION)
# ======================================
DATA_URL = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/main/Hafizah_SSES_Cleaned.csv"
df = pd.read_csv(DATA_URL)

# ======================================
# OBJECTIVE 3 VARIABLES (FINAL)
# ======================================
objective3_cols = [
    'calm_under_pressure',
    'emotional_control',
    'adaptability',
    'self_motivation',
    'task_persistence',
    'teamwork'
]

# Ensure numeric (safe check)
df[objective3_cols] = df[objective3_cols].apply(pd.to_numeric, errors="coerce")
df[objective3_cols] = df[objective3_cols].fillna(df[objective3_cols].median())

# ======================================
# 1️⃣ LIKERT DISTRIBUTION (STACKED BAR)
# ======================================
st.subheader("1. Distribution of Emotional Resilience and Personal Development Attributes")

# Prepare Likert distribution (same logic as Colab)
likert_counts = (
    df[objective3_cols]
    .apply(lambda x: x.value_counts(normalize=True))
    .T
    .reset_index()
    .rename(columns={"index": "Attribute"})
)

# Convert to long format
likert_long = likert_counts.melt(
    id_vars="Attribute",
    var_name="Likert Scale",
    value_name="Proportion"
)

# Plot stacked bar chart
fig = px.bar(
    likert_long,
    x="Attribute",
    y="Proportion",
    color="Likert Scale",
    barmode="stack",
    title="Distribution of Emotional Resilience and Personal Development Attributes"
)

fig.update_layout(
    yaxis_title="Proportion of Responses",
    xaxis_title="Attributes",
    legend_title="Likert Scale"
)

st.plotly_chart(fig, use_container_width=True)

# ======================================
# 2️⃣ RADAR CHART (AVERAGE PROFILE)
# ======================================
st.subheader("2. Average Profile of Emotional Resilience")

mean_scores = df[objective3_cols].mean()

fig2 = go.Figure()

fig2.add_trace(go.Scatterpolar(
    r=mean_scores.values.tolist() + [mean_scores.values[0]],
    theta=objective3_cols + [objective3_cols[0]],
    fill='toself'
))

fig2.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    showlegend=False,
    title="Average Emotional Resilience and Personal Development Profile"
)

st.plotly_chart(fig2, use_container_width=True)

# ======================================
# 3️⃣ CORRELATION HEATMAP
# ======================================
st.subheader("3. Correlation Between Emotional Resilience Attributes")

corr_matrix = df[objective3_cols].corr()

fig3 = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu",
    title="Correlation Between Emotional Resilience and Personal Development Attributes"
)

st.plotly_chart(fig3, use_container_width=True)

# ======================================
# 4️⃣ BOX PLOT (VARIABILITY)
# ======================================
st.subheader("4. Distribution and Variability of Emotional Resilience Attributes")

melted = df[objective3_cols].melt(
    var_name="Attribute",
    value_name="Likert Score"
)

fig4 = px.box(
    melted,
    x="Attribute",
    y="Likert Score",
    title="Distribution and Variability of Emotional Resilience Attributes"
)

st.plotly_chart(fig4, use_container_width=True)

# ======================================
# 5️⃣ GROUP COMPARISON (GENDER)
# ======================================
st.subheader("5. Comparison by Gender")

if "gender" in df.columns:
    gender_means = df.groupby("gender")[objective3_cols].mean().reset_index()

    fig5 = px.bar(
        gender_means,
        x="gender",
        y=objective3_cols,
        barmode="group",
        title="Comparison of Emotional Resilience and Personal Development by Gender"
    )

    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Gender variable is not available in the dataset.")
