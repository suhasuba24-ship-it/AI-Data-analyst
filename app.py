import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("📊 AI Data Analyst - Final Version")

uploaded = st.file_uploader("Upload your CSV file", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"✅ Uploaded! Rows: {len(df)}, Columns: {len(df.columns)}")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1. Columns")
        st.dataframe(pd.DataFrame(df.columns, columns=["Column Name"]))
    with c2:
        st.subheader("2. Quick Stats")
        st.metric("Total Rows", len(df))
        st.metric("Total Columns", len(df.columns))

    st.subheader("3. Data Preview")
    st.dataframe(df, use_container_width=True)

    st.subheader("4. Chart")
    col = st.selectbox("Select a column for analysis", df.columns)
    if col:
        st.bar_chart(df[col].value_counts())
else:
    st.info("Please upload a CSV file to start analysis")