from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from extract_text import extract_text_from_file
from groq_llm import generate_summary, answer_question, simulate_scenario
from vector_db import vector_db
from fine_tuning import fine_tuner
from typing import List, Dict, Any, Optional
import json
import os

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

class VectorSearchRequest(BaseModel):
    query: str
    n_results: int = 5

class TrainingDataRequest(BaseModel):
    instruction: str
    input_text: str
    output: str

class FineTuneRequest(BaseModel):
    training_data: List[TrainingDataRequest]
    model_name: Optional[str] = None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    filename = file.filename or "unknown_file"
    text = extract_text_from_file(filename, file_bytes)
    summary = generate_summary(text)
    
    # Store in vector database
    doc_id = vector_db.add_document(
        text=text,
        metadata={
            "filename": filename,
            "file_size": len(file_bytes),
            "upload_timestamp": str(datetime.now())
        }
    )
    
    return {
        "summary": summary, 
        "full_text": text,
        "doc_id": doc_id,
        "message": "Document uploaded and stored in vector database"
    }

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    answer = answer_question(request.context, request.question)
    return {"answer": answer}

@app.post("/simulate")
async def simulate(request: ScenarioRequest):
    result = simulate_scenario(request.context, request.scenario)
    return {"result": result}

# Vector Database Endpoints
@app.post("/vector/search")
async def search_documents(request: VectorSearchRequest):
    """Search for similar documents using vector database"""
    try:
        results = vector_db.search_similar(request.query, request.n_results)
        return {
            "query": request.query,
            "results": results,
            "total_found": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/vector/documents")
async def get_all_documents():
    """Get all documents from vector database"""
    try:
        documents = vector_db.get_all_documents()
        return {
            "documents": documents,
            "total_count": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve documents: {str(e)}")

@app.get("/vector/stats")
async def get_vector_stats():
    """Get vector database statistics"""
    try:
        stats = vector_db.get_collection_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.delete("/vector/document/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from vector database"""
    try:
        success = vector_db.delete_document(doc_id)
        if success:
            return {"message": f"Document {doc_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

# Fine-tuning Endpoints
@app.post("/fine-tune/prepare")
async def prepare_training_data(request: FineTuneRequest):
    """Prepare training data for fine-tuning"""
    try:
        # Convert to format expected by fine-tuner
        training_data = []
        for item in request.training_data:
            training_data.append({
                'instruction': item.instruction,
                'input': item.input_text,
                'output': item.output
            })
        
        # Create dataset
        dataset = fine_tuner.prepare_training_data(training_data)
        
        return {
            "message": "Training data prepared successfully",
            "dataset_size": len(dataset),
            "sample_data": training_data[:3] if len(training_data) > 3 else training_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to prepare training data: {str(e)}")

@app.post("/fine-tune/train")
async def start_fine_tuning(request: FineTuneRequest):
    """Start fine-tuning process"""
    try:
        # Prepare training data
        training_data = []
        for item in request.training_data:
            training_data.append({
                'instruction': item.instruction,
                'input': item.input_text,
                'output': item.output
            })
        
        dataset = fine_tuner.prepare_training_data(training_data)
        
        # Start training
        output_dir = f"./fine_tuned_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        model_path = fine_tuner.train(dataset, output_dir)
        
        return {
            "message": "Fine-tuning completed successfully",
            "model_path": model_path,
            "training_samples": len(training_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fine-tuning failed: {str(e)}")

@app.get("/fine-tune/generate")
async def generate_with_fine_tuned_model_get(prompt: str, max_length: int = 100):
    """Generate response using fine-tuned model (GET method)"""
    try:
        if fine_tuner.model is None:
            raise HTTPException(status_code=400, detail="No fine-tuned model loaded. Please train or load a model first.")
        
        response = fine_tuner.generate_response(prompt, max_length)
        return {
            "prompt": prompt,
            "response": response,
            "model_used": "fine_tuned"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/fine-tune/generate")
async def generate_with_fine_tuned_model_post(prompt: str, max_length: int = 100):
    """Generate response using fine-tuned model (POST method)"""
    try:
        if fine_tuner.model is None:
            raise HTTPException(status_code=400, detail="No fine-tuned model loaded. Please train or load a model first.")
        
        response = fine_tuner.generate_response(prompt, max_length)
        return {
            "prompt": prompt,
            "response": response,
            "model_used": "fine_tuned"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/fine-tune/load")
async def load_fine_tuned_model(model_path: str):
    """Load a fine-tuned model"""
    try:
        fine_tuner.load_model(model_path)
        return {
            "message": f"Model loaded successfully from {model_path}",
            "model_path": model_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

@app.post("/fine-tune/evaluate")
async def evaluate_fine_tuned_model(test_data: List[TrainingDataRequest]):
    """Evaluate the fine-tuned model"""
    try:
        if fine_tuner.model is None:
            raise HTTPException(status_code=400, detail="No model loaded for evaluation")
        
        # Convert test data
        test_converted = []
        for item in test_data:
            test_converted.append({
                'instruction': item.instruction,
                'input': item.input_text,
                'output': item.output
            })
        
        # Evaluate
        eval_results = fine_tuner.evaluate_model(test_converted)
        
        return {
            "evaluation_results": eval_results,
            "test_samples": len(test_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

# Hybrid Search Endpoint
@app.post("/hybrid/search")
async def hybrid_search(request: VectorSearchRequest):
    """Perform hybrid search using vector database and LLM"""
    try:
        # Get vector search results
        vector_results = vector_db.search_similar(request.query, request.n_results)
        
        # Combine relevant context from vector results
        context_parts = []
        for result in vector_results:
            if result['distance'] < 0.8:  # Only include relevant results
                context_parts.append(result['document'])
        
        combined_context = "\n\n".join(context_parts)
        
        # Use LLM to answer based on retrieved context
        if combined_context:
            answer = answer_question(combined_context, request.query)
        else:
            answer = "No relevant documents found in the database."
        
        return {
            "query": request.query,
            "answer": answer,
            "vector_results": vector_results,
            "context_used": combined_context[:500] + "..." if len(combined_context) > 500 else combined_context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hybrid search failed: {str(e)}")

# Import datetime for the upload endpoint
from datetime import datetime