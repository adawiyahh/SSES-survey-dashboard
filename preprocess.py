import pandas as pd
import streamlit as st
from configuration import GOOGLE_SHEET_URL

@st.cache_data(ttl=15)   # refresh every 15 seconds
def load_data():
    df = pd.read_csv(GOOGLE_SHEET_URL)
    return df

