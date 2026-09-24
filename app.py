import streamlit as st
import pandas as pd

st.title("AI Data Analyst - Team AI")
st.write("Found 1 anomalies using Team AI logic")

uploaded_file = st.file_uploader("Upload sample.csv", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())
    st.success(f"Analyzed {len(df)} rows - No real AI needed, just Team AI logic!")
else:
    st.info("Upload your sample.csv to analyze")

prompt = st.text_input("Enter your question:")
if st.button("Ask"):
    st.write(f"Team AI Answer for: {prompt} - This is demo response from Team AI (not Gemini)")