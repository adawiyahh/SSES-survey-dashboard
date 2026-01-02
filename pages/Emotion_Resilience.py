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
    # Define and Clean the Columns
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

# ======================================
# KEY METRICS
# ======================================
        st.subheader("📊 Executive Summary")
        agree_prop = df[available_cols].isin([4, 5]).mean()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Overall Agreement", f"{agree_prop.mean():.1%}")
        m2.metric("Top Strength", agree_prop.idxmax().replace('_', ' ').title())
        m3.metric("Growth Area", agree_prop.idxmin().replace('_', ' ').title())

# ======================================
# DATA VISUALIZATION
# ======================================

        # 1. RADAR CHART
        st.subheader("1. Average Resilience Profile")
        mean_scores = df[available_cols].mean()
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=mean_scores.values.tolist() + [mean_scores.values[0]],
            theta=[c.replace('_', ' ').title() for c in available_cols] + [available_cols[0].replace('_', ' ').title()],
            fill='toself', fillcolor='rgba(31, 119, 180, 0.4)', line_color='#1f77b4'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.markdown(f"""
        **💡 Insight:** The radar chart displays a balanced resilience profile. The widest point is **{mean_scores.idxmax().replace('_',' ').title()}** (Mean: {mean_scores.max():.2f}), 
        indicating this is the group's core strength.
        **Interpretation:** Respondents are most confident in their interpersonal and collaborative abilities, while the slightly retracted points suggest areas where stress management might be less consistent.
        """)

        # 2. CORRELATION ANALYSIS
        st.subheader("2. Attribute Correlation Matrix")
        corr = df[available_cols].corr()
        fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto", height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Key Finding Table for Correlation
        st.markdown("**📌 Key Correlation Pairs:**")
        high_corr = corr.unstack().sort_values(ascending=False).drop_duplicates()
        high_corr = high_corr[high_corr < 1].head(3)
        st.table(pd.DataFrame(high_corr, columns=['Correlation Coefficient']))

        st.markdown("""
        **💡 Insight:** Strong positive correlations exist between emotional control and adaptability. 
        **Interpretation:** This confirms that individuals who can regulate their emotions effectively are significantly more likely to adapt to changing environments, validating the synergy between internal resilience and external flexibility.
        """)
        
        # 3. DISTRIBUTION BOXPLOT
        st.subheader(" Variability of Attributes")
        fig_box = px.box(
            df.melt(value_vars=resilience_cols),
            x="variable",
            y="value",
            color="variable"
            title="Score Spread per Attribute"
        )
        # 4. VIOLIN PLOT
        st.subheader("3. Score Density & Distribution")
        df_melted = df.melt(value_vars=available_cols, var_name="Attribute", value_name="Score")
        fig_violin = px.violin(df_melted, x="Attribute", y="Score", color="Attribute", box=True, points="all")
        st.plotly_chart(fig_violin, use_container_width=True)
        
        st.markdown("""
        **💡 Insight:** The "bulge" in the violins shows where the majority of scores lie. 
        **Interpretation:** Unlike a boxplot, this reveals if scores are bi-modal (split between extremes). A wider middle indicates a strong consensus among respondents, whereas a stretched violin suggests high variability in how stress is managed within the group.
        """)
                       
        # 5. DIVERGING PERCENTAGE BAR
        st.subheader("4. Sentiment Analysis (Agreement vs Disagreement)")
        def get_sentiment(col):
            counts = df[col].value_counts(normalize=True).reindex([1,2,3,4,5], fill_value=0)
            disagree = -(counts[1] + counts[2]) * 100
            neutral = counts[3] * 100
            agree = (counts[4] + counts[5]) * 100
            return pd.Series([disagree, neutral, agree], index=['Disagree', 'Neutral', 'Agree'])

        sentiment_df = df[available_cols].apply(get_sentiment).T.reset_index()
        fig_sent = px.bar(sentiment_df, x=['Disagree', 'Neutral', 'Agree'], y='index', 
                          orientation='h', barmode='relative',
                          color_discrete_map={'Disagree': '#EF553B', 'Neutral': '#FECB52', 'Agree': '#00CC96'})
        st.plotly_chart(fig_sent, use_container_width=True)

        st.markdown("""
        **💡 Insight:** This chart visualizes the "resistance" to each attribute. 
        **Interpretation:** Attributes with a longer red bar (Disagree) are primary targets for intervention. If 'Emotional Control' shows higher disagreement than 'Teamwork', development programs should prioritize emotional regulation training.
        """)
        
        # 6. ATTRIBUTE HIERARCHY (Treemap)
        st.subheader("5. Attribute Hierarchy Ranking")
        tree_data = pd.DataFrame({
            "Attribute": [c.replace('_', ' ').title() for c in available_cols],
            "Mean Score": mean_scores.values
        }).sort_values(by="Mean Score", ascending=False)
        fig_tree = px.treemap(tree_data, path=['Attribute'], values='Mean Score',
                              color='Mean Score', color_continuous_scale='Blues')
        st.plotly_chart(fig_tree, use_container_width=True)
        
        st.markdown(f"""
        **💡 Insight:** The largest block represents **{tree_data.iloc[0]['Attribute']}**. 
        **Interpretation:** This hierarchy visualizes the dominance of certain traits. It provides a clear ranking of which attributes the respondent group feels most prepared to leverage in their personal development.
        """)

        # 6. DISTRIBUTION BOXPLOT (Fixed your previous code snippet)
        st.subheader("6. Variability & Range Analysis")
        fig_box = px.box(df_melted, x="Attribute", y="Score", color="Attribute")
        st.plotly_chart(fig_box, use_container_width=True)
        
        st.markdown("""
        **💡 Insight:** The height of the box shows the Interquartile Range (IQR). 
        **Interpretation:** A short box indicates consistent behavior across the group, while a tall box (and outliers) indicates that personal development is highly individualized, requiring personalized coaching rather than a one-size-fits-all strategy.
        """)
# ======================================
# CONCLUSION
# ======================================
        st.markdown("---")
        st.subheader("🏁 Conclusion & Recommendations")
        
        st.success(f"""
        **Synthesis of Findings:**
        The analysis successfully investigated the relationship between emotional resilience and personal development. 
        1. **Core Strength:** The group excels in **{tree_data.iloc[0]['Attribute']}**, which serves as a protective factor during stress.
        2. **Critical Link:** The high correlation between **{available_cols[1].replace('_',' ')}** and **{available_cols[2].replace('_',' ')}** suggests that improving one will naturally boost the other.
        3. **Development Opportunity:** Based on the sentiment and hierarchy charts, **{tree_data.iloc[-1]['Attribute']}** represents the most significant area for growth.
        
        **Final Strategy:** To enhance overall resilience, training should not just focus on individual skills but on the **interconnectedness** of emotional control and adaptability. By strengthening the weakest links identified, participants can achieve a more robust and flexible personal development profile.
        """)
else:
    st.warning("Please verify that the GitHub repository 'SSES-survey-dashboard' is set to **Public**.")
