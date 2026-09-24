import streamlit as st
import pandas as pd
import speech_recognition as sr
from gtts import gTTS
import io
import tempfile
import os

st.set_page_config(page_title="AI Data Analyst with Voice", layout="wide")
st.title("AI Data Analyst + Voice Assistant")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 1. Columns")
    st.write(df.columns.tolist())
    st.write("### 2. Data Preview")
    st.dataframe(df)

    st.write("### 3. Chart")
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    if numeric_cols:
        selected_col = st.selectbox("Select a column for analysis", numeric_cols)
        if "Name" in df.columns:
            st.bar_chart(df.set_index("Name")[selected_col])
        else:
            st.bar_chart(df[selected_col])

    st.divider()
    st.subheader("Voice Assistant")
    audio_value = st.audio_input("Ask: What is average of salary?")

    if audio_value:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_value.getvalue())
            tmp_path = tmp.name

        r = sr.Recognizer()
        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)
                st.success(f"You asked: {text}")

                text_lower = text.lower()
                found_col = None
                for col in df.columns:
                    if col.lower() in text_lower:
                        found_col = col
                        break

                # Logic with Column Not Exist
                if found_col:
                    if found_col in numeric_cols:
                        if "average" in text_lower or "mean" in text_lower:
                            answer = f"Average {found_col} is {df[found_col].mean():.2f}"
                        elif "sum" in text_lower or "total" in text_lower:
                            answer = f"Total {found_col} is {df[found_col].sum():.2f}"
                        elif "max" in text_lower:
                            answer = f"Maximum {found_col} is {df[found_col].max()}"
                        elif "min" in text_lower:
                            answer = f"Minimum {found_col} is {df[found_col].min()}"
                        else:
                            answer = f"Average {found_col} is {df[found_col].mean():.2f}"
                    else:
                        answer = f"Column '{found_col}' is not numeric."
                elif any(w in text_lower for w in ["average", "mean", "sum", "total", "max", "min"]):
                    # User asked for calculation but column not found
                    guessed = text_lower.split("of")[-1].strip() if "of" in text_lower else "that column"
                    answer = f"Column '{guessed}' does not exist. Available columns are: {', '.join(df.columns)}"
                elif "how many" in text_lower or "rows" in text_lower or "count" in text_lower:
                    answer = f"Total {len(df)} rows are there."
                elif "column" in text_lower:
                    answer = f"Columns are {', '.join(df.columns)}"
                else:
                    answer = f"Column not found. Available columns are: {', '.join(df.columns)}"

                st.write(f"**AI Answer:** {answer}")

                tts = gTTS(text=answer, lang='en')
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                st.audio(mp3_fp, format="audio/mp3")

        except Exception as e:
            st.error(f"Could not understand voice: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
else:
    st.info("Please upload a CSV file.")