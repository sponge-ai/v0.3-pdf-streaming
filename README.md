# README

Demo pipeline to allow user to ask prompt about uploaded PDF file.

Uses OpenAI's Files and Responses API to upload, then read the PDF.

```sh
# create virtual env
python3 -m venv .venv
source .venv/bin/activate

# install deps
pip install fastapi uvicorn python-multipart typing openai dotenv

# run server
uvicorn server:app --reload
```
