from fastapi import FastAPI, UploadFile, File, Form, WebSocket
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
import io

app = FastAPI()
dataframes = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>Dynamic BI Platform</h1>
    <p>Use the API or /docs endpoint to interact.</p>
    """

@app.post("/upload_csv/")
async def upload_csv(user_id: str = Form(...), file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    dataframes[user_id] = df
    return {"message": "CSV uploaded", "columns": list(df.columns)}

@app.post("/chat/")
async def chat(user_id: str = Form(...), message: str = Form(...)):
    df = dataframes.get(user_id)
    if df is not None:
        column_list = ", ".join(df.columns)
        answer = f"You said: '{message}'. Your dataset columns are: {column_list}"
    else:
        answer = "No data found. Please upload a CSV first."
    return {"response": answer}

@app.get("/plot/")
async def plot(user_id: str, x: str, y: str):
    df = dataframes.get(user_id)
    if df is None:
        return {"error": "No data found"}
    fig = px.line(df, x=x, y=y, title=f"{y} vs {x}")
    return fig.to_json()

