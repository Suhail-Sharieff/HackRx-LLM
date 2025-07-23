from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from extract_text import extract_text_from_file
from groq_llm import generate_summary, answer_question, simulate_scenario

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

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = extract_text_from_file(file.filename, file_bytes)
    summary = generate_summary(text)
    return {"summary": summary, "full_text": text}

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    answer = answer_question(request.context, request.question)
    return {"answer": answer}

@app.post("/simulate")
async def simulate(request: ScenarioRequest):
    result = simulate_scenario(request.context, request.scenario)
    return {"result": result}
