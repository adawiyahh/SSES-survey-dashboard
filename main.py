import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from preprocess import load_data
from pages import Emotional_Resilience

# ======================================
# PAGE CONFIG 
# ======================================
st.set_page_config(
    page_title="SSES Survey Dashboard",
    page_icon="📊",
    layout="wide"
)

# Define page
homepage = st.Page("Homepage.py",title=" Homepage")
demographic = st.Page("Demographic_Analysis.py",title="Demographic Analysis")
machine_learning = st.Page("Machine_Learning.py",title="Machine Learning")
survey = st.Page("Survey_Charts.py",title="Survey Chart")
emotion = st.Page("Emotion_Resilience.py",title="Emotion Resilience")

# ======================================
# NAVIGATION MENU
# ======================================
pg = st.navigation(
    {
        "Menu": [homepage, demographic, machine_learning, survey, emotion]
    }
)

pg.run

# ======================================
# BACKGROUND IMAGE FUNCTIONS
# ======================================
def get_base64_image(image_path):
    if not Path(image_path).exists():
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_base64):
    if image_base64 is None:
        return
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 14px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ======================================
# APPLY BACKGROUND
# ======================================
BASE_DIR = Path(os.getcwd())
IMAGE_PATH = BASE_DIR / "assets" / "sses_background.jpg"
bg_image = get_base64_image(str(IMAGE_PATH))
set_background(bg_image)

# ======================================
# TITLE
# ======================================
st.title("SSES Survey Dashboard")
st.markdown("""
An interactive dashboard for analysing **emotional resilience and personal development**
based on the SSES survey responses.
""")

# ======================================
# LOAD DATA (SHARED SOURCE)
# ======================================
df = load_data()

# ======================================
# OVERVIEW SECTION
# ======================================
st.subheader("📌 Dashboard Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", len(df))
col2.metric("Total Variables", df.shape[1])
col3.metric("Missing Values", df.isna().sum().sum())

# ======================================
# DATA PREVIEW
# ======================================
with st.expander("🔍 View Dataset Preview"):
    st.dataframe(df, use_container_width=True)

# ======================================
# SUMMARY STATISTICS
# ======================================
with st.expander("📈 View Summary Statistics"):
    st.write(df.describe(include="all"))

# ======================================
# NAVIGATION INFO
# ======================================
st.markdown("""
### 📂 Available Analysis Pages
Use the **sidebar** to navigate between analysis pages:

- 👥 Demographic Analysis
- 📊 Survey Charts
- 🤖 Machine Learning
- 🎯 Emotional Resilience Analysis *(Main Project Page)*
""")
