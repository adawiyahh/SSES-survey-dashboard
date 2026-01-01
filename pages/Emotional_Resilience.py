import streamlit as st
import plotly.express as px
import pandas as pd

from preprocess import load_data

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="Emotional Resilience Analysis",
    layout="wide"
)

# ======================================
# LOAD DATA (shared group dataset)
# ======================================
df = load_data()

# ======================================
# PAGE TITLE & OBJECTIVE
# ======================================
st.title("Emotional Resilience and Personal Development")

st.markdown("""
**Objective:**  
To investigate the relationship between emotional resilience and personal development attributes,
including motivation, adaptability, emotional control, task persistence, and teamwork skills.
""")

# ======================================
# STEP 4: DEFINE OBJECTIVE 3 VARIABLES
# ======================================
objective3_cols = [
    'calm_under_pressure',
    'emotional_control',
    'adaptability',
    'self_motivation',
    'task_persistence',
    'teamwork'
]

available_cols = [c for c in objective3_cols if c in df.columns]

if len(available_cols) < 2:
    st.warning("Required variables for Emotional Resilience analysis are not available.")
    st.stop()

# ======================================
# STEP 5: SCIENTIFIC VISUALIZATIONS
# ======================================

# 1️⃣ Likert Distribution
st.subheader("1. Distribution of Emotional Resilience Attributes")

selected_attr = st.selectbox(
    "Select an attribute",
    options=available_cols
)

value_counts = df[selected_attr].value_counts().reset_index()
value_counts.columns = [selected_attr, "Count"]

fig1 = px.bar(
    value_counts,
    x=selected_attr,
    y="Count",
    text="Count",
    title=f"Response Distribution for {selected_attr}"
)

st.plotly_chart(fig1, use_container_width=True)


# 2️⃣ Radar Chart
st.subheader("2. Average Personal Development Profile")

mean_scores = df[available_cols].mean().reset_index()
mean_scores.columns = ["Attribute", "Mean Score"]

fig2 = px.line_polar(
    mean_scores,
    r="Mean Score",
    theta="Attribute",
    line_close=True,
    title="Average Emotional Resilience and Personal Development Profile"
)

st.plotly_chart(fig2, use_container_width=True)


# 3️⃣ Correlation Heatmap
st.subheader("3. Correlation Between Attributes")

corr = df[available_cols].corr()

fig3 = px.imshow(
    corr,
    text_auto=".2f",
    title="Correlation Heatmap of Emotional Resilience Attributes"
)

st.plotly_chart(fig3, use_container_width=True)


# 4️⃣ Box Plot
st.subheader("4. Distribution and Variability")

melted = df[available_cols].melt(
    var_name="Attribute",
    value_name="Score"
)

fig4 = px.box(
    melted,
    x="Attribute",
    y="Score",
    title="Variability of Emotional Resilience and Development Attributes"
)

st.plotly_chart(fig4, use_container_width=True)


# 5️⃣ Group Comparison (Gender)
st.subheader("5. Comparison by Gender")

if 'gender' in df.columns:
    gender_means = df.groupby('gender')[available_cols].mean().reset_index()

    fig5 = px.bar(
        gender_means,
        x="gender",
        y=available_cols,
        barmode="group",
        title="Emotional Resilience Attributes by Gender"
    )

    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Gender variable is not available for group comparison.")
