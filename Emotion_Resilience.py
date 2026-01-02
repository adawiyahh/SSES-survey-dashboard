import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def app():
    # ======================================
    # PAGE TITLE & PROBLEM STATEMENT
    # ======================================
    st.title("Emotional Resilience and Personal Development")

    st.markdown("""
    **Problem Statement:**  
    Emotional resilience is a key factor in personal and professional success. Understanding how individuals manage stress, adapt to change, control emotions, and maintain motivation can help identify areas for personal development. This analysis investigates the relationship between emotional resilience and key personal development attributes such as adaptability, motivation, emotional control, task persistence, and teamwork skills. Insights from this study aim to inform strategies for enhancing resilience among participants.
    """)

    st.markdown("""
    **Objective:**  
    To investigate the relationship between emotional resilience and personal development attributes, including motivation, adaptability, emotional control, task persistence, and teamwork skills.
    """)

    # ======================================
    # LOAD CLEANED DATASET
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

    # Ensure numeric and handle missing values
    df[objective3_cols] = df[objective3_cols].apply(pd.to_numeric, errors="coerce")
    df[objective3_cols] = df[objective3_cols].fillna(df[objective3_cols].median())

    # ======================================
    # 🧾 SUMMARY OVERVIEW – LIKERT DISTRIBUTION
    # ======================================
    st.markdown("### 🧾 Summary Overview")

    agree_levels = [4, 5]
    disagree_levels = [1, 2]

    agree_prop = df[objective3_cols].isin(agree_levels).mean()
    disagree_prop = df[objective3_cols].isin(disagree_levels).mean()

    strongest_attr = agree_prop.idxmax()
    weakest_attr = agree_prop.idxmin()
    overall_resilience = agree_prop.mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Agreement Level", f"{overall_resilience:.2%}")
    col2.metric("Strongest Attribute", strongest_attr.replace("_", " ").title())
    col3.metric("Lowest Agreement Attribute", weakest_attr.replace("_", " ").title())

    # Insight box
    st.markdown(
        f"""
        <div style="
            background-color:#f7f9fb;
            padding:18px;
            border-radius:10px;
            border-left:5px solid #4CAF50;
        ">
        <b>Interpretation:</b><br>
        The Likert-scale distribution indicates that respondents generally demonstrate a positive level of emotional
        resilience and personal development. The highest level of agreement is observed for
        <b>{strongest_attr.replace("_", " ").title()}</b>, while
        <b>{weakest_attr.replace("_", " ").title()}</b> shows comparatively lower agreement,
        suggesting a potential area for development.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================================
    # 1️⃣ LIKERT DISTRIBUTION (STACKED BAR)
    # ======================================
    st.subheader("1. Distribution of Emotional Resilience and Personal Development Attributes")

    likert_counts = df[objective3_cols].apply(lambda x: x.value_counts(normalize=True)).T.reset_index().rename(columns={"index": "Attribute"})
    likert_long = likert_counts.melt(id_vars="Attribute", var_name="Likert Scale", value_name="Proportion")

    fig = px.bar(
        likert_long,
        x="Attribute",
        y="Proportion",
        color="Likert Scale",
        barmode="stack",
        title="Distribution of Emotional Resilience and Personal Development Attributes"
    )
    fig.update_layout(yaxis_title="Proportion of Responses", xaxis_title="Attributes", legend_title="Likert Scale")
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

    melted = df[objective3_cols].melt(var_name="Attribute", value_name="Likert Score")
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
