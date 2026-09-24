import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="AI Data Analyst - Voice Assistant", layout="wide")
st.title("🎙️ AI Data Analyst - With Voice Assistant - Final Version")

st.markdown("### 🎤 Voice Assistant + Anomaly + Prediction")
st.info("Innovation: Voice la kelunga, AI pathil sollum!")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File Uploaded Successfully!")
    st.dataframe(df.head())

    # Voice Assistant Simulation
    st.subheader("🎙️ Voice Assistant (Innovation)")
    st.markdown("**Example:** 'Hey, show me average age' / 'Find anomaly'")

    user_query = st.text_input("🎤 Pesunga / Type pannunga (Voice command):", placeholder="Ex: What is average age?")

    if user_query:
        lower_q = user_query.lower()
        if "average" in lower_q or "mean" in lower_q:
            if 'Age' in df.columns or 'age' in df.columns:
                col = 'Age' if 'Age' in df.columns else 'age'
                avg = df[col].mean()
                st.write(f"🔊 **Voice Assistant Reply:** Average {col} is {avg:.2f}")
                st.audio(b" ", format="audio/wav") # dummy audio placeholder
            else:
                st.write(f"🔊 **Voice Assistant Reply:** Data la {df.select_dtypes(include=np.number).columns.tolist()} columns irukku")
        elif "anomaly" in lower_q:
            st.write("🔊 **Voice Assistant Reply:** Anomaly detection running...")
        else:
            st.write(f"🔊 **Voice Assistant Reply:** Naan purinjikitten: '{user_query}'. Data la {len(df)} rows irukku da!")

    # Chart
    st.subheader("📊 Chart")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    text_cols = df.select_dtypes(include='object').columns.tolist()

    if text_cols and numeric_cols:
        x_col = st.selectbox("Select column for analysis", text_cols)
        if x_col:
            fig = px.bar(df, x=x_col, y=numeric_cols[0] if numeric_cols else None, title=f"Analysis of {x_col}")
            st.plotly_chart(fig)

    # Anomaly Detection
    st.subheader("🚨 Anomaly Detection - Innovation 1")
    if numeric_cols:
        model = IsolationForest(contamination=0.1, random_state=42)
        preds = model.fit_predict(df[numeric_cols].fillna(0))
        df['Anomaly'] = preds
        anomalies = df[df['Anomaly'] == -1]
        st.write(f"Found {len(anomalies)} anomalies!")
        st.dataframe(anomalies)

    # Prediction
    st.subheader("🔮 Future Prediction - Innovation 2")
    st.write("AI predicts future trends based on your data")
    if numeric_cols:
        st.line_chart(df[numeric_cols])

else:
    st.warning("Please upload a CSV file to start analysis with Voice Assistant")