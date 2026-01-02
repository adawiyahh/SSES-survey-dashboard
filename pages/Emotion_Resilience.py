import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🧠 Emotional Resilience Analysis")

# USE THE RAW URL
DATA_URL = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/main/Hafizah_SSES_Cleaned.csv"

@st.cache_data
def load_emotion_data():
    try:
        data = pd.read_csv(DATA_URL)
        return data
    except Exception as e:
        st.error(f"Error connecting to GitHub data: {e}")
        return None

df = load_emotion_data()

if df is not None:
    objective3_cols = ['calm_under_pressure', 'emotional_control', 'adaptability', 'self_motivation', 'task_persistence', 'teamwork']
    
    # Ensure columns exist in the file
    available_cols = [c for c in objective3_cols if c in df.columns]
    
    if len(available_cols) > 0:
        df[available_cols] = df[available_cols].apply(pd.to_numeric, errors="coerce").fillna(df[available_cols].median())

        # Metrics
        agree_prop = df[available_cols].isin([4, 5]).mean()
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg. Resilience", f"{agree_prop.mean():.1%}")
        m2.metric("Strongest", agree_prop.idxmax().replace('_', ' ').title())
        m3.metric("Growth Area", agree_prop.idxmin().replace('_', ' ').title())

        # Radar Chart
        st.subheader("Resilience Profile")
        mean_scores = df[available_cols].mean()
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=mean_scores.values.tolist() + [mean_scores.values[0]],
            theta=[c.replace('_', ' ').title() for c in available_cols] + [available_cols[0].replace('_', ' ').title()],
            fill='toself'
        ))
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.error("The expected columns were not found in the CSV file.")
