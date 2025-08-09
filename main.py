from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from extract_text import extract_text_from_file
from groq_llm import generate_summary, answer_question, simulate_scenario
from typing import List
import requests
import asyncio
import os
from datetime import datetime
# from mangum import Mangum

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    context: str
    question: str

class ScenarioRequest(BaseModel):
    context: str
    scenario: str

class HackRxRunRequest(BaseModel):
    documents: str
    questions: List[str]

class HackRxRunResponse(BaseModel):
    answers: List[str]

API_KEY = os.getenv("HACKRX_API_KEY", "a8f2e613b3a3b9b825f96951bc7ed46ccded181d1c9c83205e6a395e92c71f56")  # replace with secure key or env var

def verify_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

@app.post("/hackrx/run", response_model=HackRxRunResponse)
async def hackrx_run(request_data: HackRxRunRequest, auth=Depends(verify_token)):
    try:
        # Download the document
        pdf_response = requests.get(request_data.documents)
        if pdf_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download document")

        filename = request_data.documents.split("/")[-1].split("?")[0]
        file_bytes = pdf_response.content
        text = extract_text_from_file(filename, file_bytes)

        answers = []
        for question in request_data.questions:
            answer = await try_answer_with_retry(text, question)
            answers.append(answer)
            await asyncio.sleep(1)  # prevent hitting rate limits

        return {"answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process: {str(e)}")

async def try_answer_with_retry(context: str, question: str, max_retries: int = 3) -> str:
    backoff = 2
    for attempt in range(1, max_retries + 1):
        try:
            return answer_question(context, question)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries:
                print(f"[WARN] Rate limit hit, retrying in {backoff} seconds... (Attempt {attempt})")
                await asyncio.sleep(backoff)
                backoff *= 2
            else:
                print(f"[ERROR] Failed after {attempt} attempts: {e}")
                return "Failed to answer due to rate limiting or internal error."
    return "Failed to answer due to unknown error."

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    filename = file.filename or "unknown_file"
    text = extract_text_from_file(filename, file_bytes)
    summary = generate_summary(text)
    return {
        "summary": summary,
        "full_text": text,
        "file_size": len(file_bytes),
        "upload_timestamp": str(datetime.now())
    }

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    answer = answer_question(request.context, request.question)
    return {"answer": answer}

@app.post("/simulate")
async def simulate(request: ScenarioRequest):
    result = simulate_scenario(request.context, request.scenario)
    return {"result": result}

# handler = Mangum(app)
