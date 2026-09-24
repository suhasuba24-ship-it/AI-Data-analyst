import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
import io, tempfile, os

st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("🤖 AI-Powered Data Analyst")

# --- CONFIGURE GEMINI ---
# Paste your key here
GEMINI_API_KEY = "PASTE_YOUR_GEMINI_KEY_HERE" 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())
    
    # --- AI FEATURE 1: ANOMALY DETECTION ---
    st.subheader("1. AI Anomaly Detection (Isolation Forest)")
    numeric_df = df.select_dtypes(include=['int64','float64'])
    if not numeric_df.empty:
        iso = IsolationForest(contamination=0.05)
        df['Anomaly'] = iso.fit_predict(numeric_df)
        anomalies = df[df['Anomaly'] == -1]
        st.write(f"Found {len(anomalies)} anomalies using AI")
        st.dataframe(anomalies)
    
    # --- AI FEATURE 2: AUTO INSIGHTS ---
    st.subheader("2. AI Auto Insights")
    if st.button("Generate AI Insights"):
        prompt = f"You are a data analyst. Give 3 bullet point insights for this data: {df.head().to_string()} Columns: {list(df.columns)}"
        response = model.generate_content(prompt)
        st.write(response.text)
        
    # --- AI FEATURE 3: VOICE + LLM Q&A ---
    st.divider()
    st.subheader("3. AI Voice Assistant (with LLM Brain)")
    st.write("Ask anything: 'Which employee has highest salary? Why is sales low?'")
    
    query = st.text_input("Or Type your question:")
    audio_value = st.audio_input("Or Speak")

    final_question = None
    if audio_value:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_value.getvalue())
            tmp_path = tmp.name
        r = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio_data = r.record(source)
            try:
                final_question = r.recognize_google(audio_data)
                st.success(f"You asked: {final_question}")
            except: pass
        os.remove(tmp_path)
    
    if query:
        final_question = query

    if final_question:
        # Check if column exists first
        found = False
        for col in df.columns:
            if col.lower() in final_question.lower():
                found = True
        
        if not found and any(w in final_question.lower() for w in ["average","sum","max","min","salary","age"]):
             answer = f"Column does not exist. Available columns are: {', '.join(df.columns)}"
        else:
            # REAL AI ANSWER using LLM
            prompt = f"Dataset: {df.to_string()}\n\nQuestion: {final_question}\nAnswer based on data, if column not present say Column does not exist."
            response = model.generate_content(prompt)
            answer = response.text

        st.write(f"**AI Answer:** {answer}")
        tts = gTTS(text=answer, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        st.audio(mp3_fp, format="audio/mp3")