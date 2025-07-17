# README

Added streaming with OpenAI Responses API and FastAPI StreamingResponse

```sh
# create virtual env
python3 -m venv .venv
source .venv/bin/activate

# install deps
pip install fastapi uvicorn python-multipart typing openai dotenv

# run server
uvicorn server:app --reload
```

```py
# server.py
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
```
