import streamlit as st
import pandas as pd
import speech_recognition as sr
from gtts import gTTS
import io
import tempfile
import os

st.set_page_config(page_title="Universal AI Data Analyst", layout="wide")
st.title("🤖 Universal AI Data Analyst + Voice (No API Key)")

uploaded_file = st.file_uploader("Upload ANY CSV or Excel", type=["csv", "xlsx", "xls"])

if uploaded_file:
    # Load any file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"Loaded {len(df)} rows, {len(df.columns)} columns from {uploaded_file.name}")
    st.write("### 1. Columns", list(df.columns))
    st.write("### 2. Preview")
    st.dataframe(df.head(20))

    numeric_cols = df.select_dtypes(include=['int64','float64','int32','float32']).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()

    if numeric_cols:
        st.write("### 3. Auto Chart")
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-Axis", df.columns)
        with col2:
            y_axis = st.selectbox("Y-Axis", numeric_cols)
        try:
            chart_data = df.groupby(x_axis)[y_axis].mean() if x_axis in text_cols else df[y_axis]
            st.bar_chart(chart_data)
        except:
            st.line_chart(df[y_axis])

    st.divider()
    st.subheader("🎤 Voice / Text Analyst - Works for ALL DB")

    audio_value = st.audio_input("Ask by voice: Eg - What is average salary?")
    question = st.text_input("Or type: what is sum of profit? / max marks? / how many rows?")

    voice_text = ""
    if audio_value:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_value.getvalue())
            tmp_path = tmp.name
        r = sr.Recognizer()
        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = r.record(source)
                voice_text = r.recognize_google(audio_data)
                st.success(f"You asked: {voice_text}")
        except Exception as e:
            st.error(f"Voice error: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    final_question = voice_text if voice_text else question

    if st.button("Ask AI") and final_question:
        q_lower = final_question.lower()
        answer = ""
        found_col = None

        # Find which column user is asking about - works even with spaces
        for col in df.columns:
            if col.lower() in q_lower:
                found_col = col
                break

        # Also check without spaces
        if not found_col:
            q_nospace = q_lower.replace(" ", "")
            for col in df.columns:
                if col.lower().replace(" ", "") in q_nospace:
                    found_col = col
                    break

        if found_col:
            if found_col in numeric_cols:
                if "average" in q_lower or "mean" in q_lower:
                    answer = f"Average of {found_col} is {df[found_col].mean():.2f}"
                elif "sum" in q_lower or "total" in q_lower:
                    answer = f"Total of {found_col} is {df[found_col].sum():.2f}"
                elif "max" in q_lower or "maximum" in q_lower or "highest" in q_lower:
                    answer = f"Maximum of {found_col} is {df[found_col].max()}"
                elif "min" in q_lower or "minimum" in q_lower or "lowest" in q_lower:
                    answer = f"Minimum of {found_col} is {df[found_col].min()}"
                elif "count" in q_lower:
                    answer = f"Count of {found_col} is {df[found_col].count()}"
                else:
                    answer = f"Found {found_col}. Average is {df[found_col].mean():.2f}, Total is {df[found_col].sum():.2f}"
            else:
                # Text column
                if "count" in q_lower or "how many" in q_lower:
                    answer = f"Unique values in {found_col}: {df[found_col].nunique()}. Top value is {df[found_col].mode()[0]}"
                else:
                    answer = f"Column '{found_col}' is text column. Unique values: {', '.join(map(str, df[found_col].unique()[:5]))}"
        else:
            # No column found
            if any(w in q_lower for w in ["average","mean","sum","total","max","min","highest","lowest"]):
                guessed = final_question.split("of")[-1].strip() if "of" in final_question.lower() else final_question
                answer = f"Column '{guessed}' does not exist. Available columns are: {', '.join(df.columns)}"
            elif "how many" in q_lower or "rows" in q_lower or "count" in q_lower:
                answer = f"Total {len(df)} rows are there. Columns are {', '.join(df.columns)}"
            elif "column" in q_lower or "columns" in q_lower:
                answer = f"Available columns are: {', '.join(df.columns)}. Numeric columns: {', '.join(numeric_cols)}"
            else:
                answer = f"Please ask about columns: {', '.join(df.columns)}"

        st.success(f"**AI Answer:** {answer}")

        # Voice output
        try:
            tts = gTTS(text=answer, lang='en')
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            st.audio(mp3_fp, format="audio/mp3")
        except:
            pass

else:
    st.info("Upload any CSV or Excel - Example: sales.csv, employee.xlsx, student database - ANY file will work!")
