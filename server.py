from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return FileResponse("static/main.html")

@app.post("/upload")
async def post_response(
    file: UploadFile = File(...), 
    prompt: Optional[str] = Form("Summarize this file: ")
):
    client = OpenAI()
    
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
        ]
    )

    return response.output[0].content[0].text