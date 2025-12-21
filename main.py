import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from preprocess import load_data

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="SSES Survey Dashboard",
    layout="wide"
)

st.title("SSES Survey Dashboard")
st.write("Monitoring survey responses in real time.")

# ----------------------------------
# Load Data
# ----------------------------------
df = load_data()

# ----------------------------------
# Sidebar Navigation (Dropdown)
# ----------------------------------
page = st.sidebar.selectbox(
    "HomePage",
    [
        "🏠 Overview",
        "👥 Demographic Analysis",
        "📊 Survey Charts",
        "🤖 Machine Learning"
    ]
)

# ==================================
# 🏠 OVERVIEW PAGE
# ==================================
if page == "🏠 Overview":
    st.subheader("📌 Dashboard Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Responses", len(df))
    col2.metric("Total Variables", len(df.columns))
    col3.metric("Missing Values", df.isna().sum().sum())

    st.markdown("### Survey Data Preview")
    st.dataframe(df, use_container_width=True)

    st.markdown("### Summary Statistics")
    st.write(df.describe(include="all"))

# ==================================
# 👥 DEMOGRAPHIC ANALYSIS PAGE
# ==================================
elif page == "👥 Demographic Analysis":
    st.subheader("👥 Demographic Analysis")

    st.info("Select a demographic variable to explore respondent distribution.")

    demo_col = st.selectbox(
        "Select Demographic Column",
        options=df.columns
    )

    fig = px.pie(
        df,
        names=demo_col,
        title=f"Distribution of {demo_col}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================
# 📊 SURVEY CHARTS PAGE
# ==================================
elif page == "📊 Survey Charts":
    st.subheader("📊 Survey Question Analysis")

    question_col = st.selectbox(
        "Select Survey Question",
        options=df.columns
    )

    value_counts = df[question_col].value_counts().reset_index()
    value_counts.columns = [question_col, "Count"]

    fig = px.bar(
        value_counts,
        x=question_col,
        y="Count",
        text="Count",
        title=f"Response Distribution for {question_col}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================
# 🤖 MACHINE LEARNING PAGE
# ==================================
elif page == "🤖 Machine Learning":
    st.subheader("🤖 Machine Learning: Respondent Segmentation")

    st.markdown("""
    **Objective:**  
    Segment respondents based on numeric survey responses using **K-Means clustering**.
    """)

    numeric_df = df.select_dtypes(include=["int64", "float64"])

    if numeric_df.shape[1] < 2:
        st.warning("At least two numeric columns are required for clustering.")
    else:
        k = st.slider("Select number of clusters (k)", 2, 6, 3)

        model = KMeans(n_clusters=k, random_state=42)
        clusters = model.fit_predict(numeric_df)

        clustered_df = numeric_df.copy()
        clustered_df["Cluster"] = clusters

        fig = px.scatter(
            clustered_df,
            x=clustered_df.columns[0],
            y=clustered_df.columns[1],
            color="Cluster",
            title="K-Means Clustering of Survey Respondents"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Clustered Data Preview")
        st.dataframe(clustered_df.head(), use_container_width=True)
