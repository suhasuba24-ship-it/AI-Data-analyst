import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
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
    # Fixed chart logic - only numeric columns
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    selected_col = st.selectbox("Select a column for analysis", numeric_cols)
    
    if "Name" in df.columns:
        st.bar_chart(df.set_index("Name")[selected_col])
    else:
        st.bar_chart(df[selected_col])

    st.divider()
    st.subheader("Voice Assistant")
    
    audio_value = st.audio_input("Click mic and ask: 'What is average sales?' or 'How many rows?'")

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
                
                if "average" in text_lower and "sales" in text_lower and "Sales" in df.columns:
                    answer = f"Average Sales is {df['Sales'].mean():.2f}"
                elif "average" in text_lower and "age" in text_lower and "Age" in df.columns:
                    answer = f"Average Age is {df['Age'].mean():.2f}"
                elif "how many" in text_lower or "rows" in text_lower or "count" in text_lower:
                    answer = f"Total {len(df)} rows are there."
                elif "column" in text_lower:
                    answer = f"Columns are {', '.join(df.columns)}"
                else:
                    answer = f"You asked about {text}. I found {len(df)} rows in the data."

                st.write(f"**AI Answer:** {answer}")

                # Convert answer to voice
                tts = gTTS(text=answer, lang='en')
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                st.audio(mp3_fp, format="audio/mp3")

        except Exception as e:
            st.error(f"Could not understand voice. Try again. Error: {e}")
        finally:
            os.remove(tmp_path)
else:
    st.info("Please upload a CSV file to start.")