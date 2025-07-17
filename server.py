from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import time
load_dotenv()

app = FastAPI()
client = OpenAI()

@app.get("/")
def read_root():
    return FileResponse("static/main.html")

@app.post("/upload")
async def post_response(
    file: UploadFile = File(...), 
    prompt: Optional[str] = Form("Summarize this file: ")
):
    file_response = client.files.create(
        file = (file.filename, await file.read()),
        purpose = "user_data"
    )
    
    file_id = file_response.id

    response = client.responses.create(
        model = "gpt-4o",
        input = [
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": prompt },
                    { "type": "input_file", "file_id": file_id }
                ]
            }
        ],
        stream=True
    )

    async def generate():
        for event in response:
            if event.type == "response.output_text.delta":
                yield event.delta

    return StreamingResponse(generate(), media_type="text/plain")
    