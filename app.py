import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

st.title("AI Data Analyst")

uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("1. Column Names")
    st.write(pd.DataFrame(df.columns, columns=["Column Name"]))
    
    st.write("3. Data Preview")
    st.dataframe(df)

    st.write("4. Chart")
    selected_col = st.selectbox("Select a column for analysis", ["Age", "Sales"])
    st.bar_chart(df.set_index("Name")[selected_col])