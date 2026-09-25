from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
app = FastAPI()
current_df = None
@app.get("/")
def home():
    return {"message": "Backend Running"}
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global current_df
    content = await file.read()
    if file.filename.endswith(".csv"):
        current_df = pd.read_csv(io.BytesIO(content))
    else:
        current_df = pd.read_excel(io.BytesIO(content))
    return {"rows": len(current_df), "columns": list(current_df.columns)}
@app.get("/ask")
def ask_question(q: str):
    global current_df
    if current_df is None:
        return {"answer": "No file uploaded"}
    q_lower = q.lower()
    for col in current_df.columns:
        if col.lower() in q_lower:
            if col in current_df.select_dtypes(include='number').columns:
                return {"answer": f"Average of {col} is {current_df[col].mean():.2f}"}
            else:
                return {"answer": f"Unique values in {col}: {current_df[col].nunique()}"}
    return {"answer": f"Available columns: {', '.join(current_df.columns)}"}