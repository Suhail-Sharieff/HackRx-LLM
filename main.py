# main.py
import asyncio
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
import requests
import os
import re

# Ensure your file names match these imports
from extract_text import extract_text_from_file
from groq_llm import gemini_call
from vector_db import VectorDatabase

app = FastAPI()

class HackRxRunRequest(BaseModel):
    documents: str
    questions: List[str]

class HackRxRunResponse(BaseModel):
    answers: List[str]

API_KEY = os.getenv("HACKRX_API_KEY", "a8f2e613b3a3b9b825f96951bc7ed46ccded181d1c9c83205e6a395e92c71f56")

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

async def try_api_call_with_retry(prompt: str, max_retries: int = 3) -> str:
    backoff_time = 2
    for attempt in range(max_retries):
        try:
            return gemini_call(prompt)
        except Exception as e:
            print(f"API call attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(backoff_time)
                backoff_time *= 2
            else:
                return "Failed to get an answer from the API after multiple retries."
    return "Failed to get an answer from the API after multiple retries."

@app.post("/hackrx/run", response_model=HackRxRunResponse, dependencies=[Depends(verify_token)])
async def hackrx_run(request_data: HackRxRunRequest):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        pdf_response = requests.get(request_data.documents, headers=headers, timeout=20)
        pdf_response.raise_for_status()

        text = extract_text_from_file("downloaded_doc.pdf", pdf_response.content)
        
        vector_db = VectorDatabase()
        
        # THIS IS THE FIX FOR THE LAST ERROR
        doc_metadata = {"source": "downloaded_document"}
        vector_db.add_document(text, metadata=doc_metadata)

        answers = []
        for question in request_data.questions:
            search_results = vector_db.search_similar(query=question)
            
            if not search_results:
                answers.append("Could not find relevant information in the document.")
                continue

            context = "\n---\n".join([result['document'] for result in search_results])
            
            prompt = f"""Based only on the context provided, answer the question concisely. If the answer is not in the context, say "I could not find the answer in the document."

Context:
---
{context}
---

Question: {question}

Answer:"""
            
            answer = await try_api_call_with_retry(prompt)
            answers.append(answer)
            await asyncio.sleep(4) # Small delay to help with rate limiting

        return {"answers": answers}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download document: {e}")
    except Exception as e:
        print(f"[CRITICAL ERROR] An unhandled exception occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")