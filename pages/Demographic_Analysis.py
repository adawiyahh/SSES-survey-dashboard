import streamlit as st
import plotly.express as px
from preprocess import load_data

st.title("👥 Demographic Analysis")
st.markdown("Explore the background and characteristics of the survey respondents.")

df = load_data()

# Selection for distribution
demo_col = st.selectbox(
    "Select Demographic Variable to Visualize",
    options=['gender', 'age', 'location', 'education_level'] if 'gender' in df.columns else df.columns
)

col1, col2 = st.columns([2, 1])

with col1:
    fig = px.pie(
        df, 
        names=demo_col, 
        hole=0.4,
        title=f"Distribution of {demo_col.replace('_', ' ').title()}",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### Quick Stats")
    stats = df[demo_col].value_counts()
    st.dataframe(stats, use_container_width=True)
