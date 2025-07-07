import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from openai import OpenAI
import tempfile
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
client = OpenAI()

@app.get("/")
def index():
    return FileResponse("static/main.html")

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...), query: str = Form("Summarize this PDF")):
    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Upload PDF to OpenAI
    uploaded_file = client.files.create(
        file=open(tmp_path, "rb"),
        purpose="user_data"
    )

    # Run GPT with PDF + prompt
    response = client.chat.completions.create(
        model="gpt-4o",  # GPT-4o or similar if needed
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file_id": uploaded_file.id
                    },
                    {
                        "type": "text",
                        "text": query
                    }
                ]
            }
        ]
    )

    result = response.choices[0].message.content

    # Return as HTML
    return HTMLResponse(content=f"<html><body><h2>Result</h2><p>{result}</p></body></html>")