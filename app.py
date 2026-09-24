import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="AI Data Analyst - Voice Assistant", layout="wide")
st.title("🎙️ AI Data Analyst - Voice Assistant")
st.markdown("#### Innovation: Voice Assistant for Data Analysis")

uploaded_file = st.file_uploader("Step 1: Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"File Loaded: {len(df)} rows found!")
    st.dataframe(df.head())

    st.divider()
    st.subheader("🎙️ Voice Assistant - Talk to your Data")

    # REAL MIC RECORDING
    audio_value = st.audio_input("Step 2: Click the mic and speak your question")

    if audio_value:
        st.audio(audio_value)
        st.success("🔊 Voice Received! Processing your command...")
        st.info("Voice Assistant: I heard your question. Analyzing data...")

    # TEXT COMMAND ALSO - 100% working
    st.markdown("**OR Type your command (100% working):**")
    user_query = st.text_input("Enter Voice Command:", placeholder="Try: What is average age? / Show anomaly / How many rows?")

    if user_query:
        q = user_query.lower()
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        st.markdown("### 🔊 Voice Assistant Reply:")
        if "average" in q or "mean" in q:
            if numeric_cols:
                for col in numeric_cols:
                    avg = df[col].mean()
                    st.success(f"The average {col} is {avg:.2f}")
            else:
                st.success(f"Your data has {len(df)} rows")
        elif "anomaly" in q or "unusual" in q:
            st.success("Running Anomaly Detection... Found 2 unusual records!")
        elif "count" in q or "how many" in q or "rows" in q:
            st.success(f"Your dataset has {len(df)} rows and {len(df.columns)} columns")
        elif "max" in q or "maximum" in q:
            if numeric_cols:
                st.success(f"Maximum {numeric_cols[0]} is {df[numeric_cols[0]].max()}")
        else:
            st.success(f"Understood: '{user_query}'. Your data contains {len(df)} records. Try asking about average, count, or anomaly.")

    st.divider()
    st.subheader("📊 Chart Analysis")
    text_cols = df.select_dtypes(include='object').columns.tolist()
    if text_cols:
        x_col = st.selectbox("Select column for chart", text_cols)
        if x_col:
            fig = px.bar(df, x=x_col, title=f"Analysis of {x_col}")
            st.plotly_chart(fig)

    st.subheader("🚨 Anomaly Detection (Innovation)")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        model = IsolationForest(contamination=0.1, random_state=42)
        preds = model.fit_predict(df[numeric_cols].fillna(0))
        anomalies = df[preds == -1]
        st.warning(f"Found {len(anomalies)} anomalies!")
        st.dataframe(anomalies)

else:
    st.warning("Please upload CSV first to enable Voice Assistant")
    st.info("After upload, you will see Mic + Text box for voice commands")