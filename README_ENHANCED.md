# Parse AI - Enhanced Document Intelligence Platform

A comprehensive document processing platform with advanced AI capabilities including vector database integration and fine-tuning features.

## 🚀 Features

### Core Document Processing
- **Document Upload**: Support for PDF, images (PNG, JPG, JPEG) with OCR
- **Text Extraction**: Advanced text extraction from various file formats
- **AI Summarization**: Automatic document summarization using Groq LLM
- **Q&A System**: Ask questions about uploaded documents
- **Scenario Simulation**: Simulate different scenarios based on document content

### 🔍 Vector Database Integration
- **Semantic Search**: Find similar documents using vector embeddings
- **Document Storage**: Persistent storage with ChromaDB
- **Smart Chunking**: Intelligent text splitting for better retrieval
- **Metadata Tracking**: File information and upload timestamps
- **Hybrid Search**: Combine vector search with LLM for better answers

### 🧠 Fine-tuning Capabilities
- **Custom Model Training**: Fine-tune models on your specific data
- **Training Data Preparation**: Convert documents to training datasets
- **Model Evaluation**: Assess fine-tuned model performance
- **Model Loading**: Load and use custom fine-tuned models
- **Response Generation**: Generate responses with fine-tuned models

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR (for image processing)
- CUDA-compatible GPU (optional, for fine-tuning)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd Parse_AI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Tesseract OCR**
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **Set up environment variables**
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

5. **Start the server**
```bash
uvicorn main:app --reload
```

6. **Start the frontend** (optional)
```bash
cd frontnd
npm install
npm run dev
```

## 📚 API Endpoints

### Document Processing
- `POST /upload` - Upload and process documents
- `POST /ask` - Ask questions about documents
- `POST /simulate` - Simulate scenarios

### Vector Database
- `POST /vector/search` - Search similar documents
- `GET /vector/documents` - Get all stored documents
- `GET /vector/stats` - Get database statistics
- `DELETE /vector/document/{doc_id}` - Delete a document

### Fine-tuning
- `POST /fine-tune/prepare` - Prepare training data
- `POST /fine-tune/train` - Start fine-tuning process
- `POST /fine-tune/generate` - Generate with fine-tuned model
- `POST /fine-tune/load` - Load a fine-tuned model
- `POST /fine-tune/evaluate` - Evaluate model performance

### Advanced Search
- `POST /hybrid/search` - Hybrid search (vector + LLM)

## 🔧 Usage Examples

### Document Upload and Processing
```python
import requests

# Upload a document
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload', files=files)
    result = response.json()
    print(f"Document ID: {result['doc_id']}")
    print(f"Summary: {result['summary']}")
```

### Vector Database Search
```python
# Search for similar documents
search_data = {
    "query": "insurance claim processing",
    "n_results": 5
}
response = requests.post('http://localhost:8000/vector/search', json=search_data)
results = response.json()
print(f"Found {results['total_found']} similar documents")
```

### Fine-tuning
```python
# Prepare training data
training_data = {
    "training_data": [
        {
            "instruction": "Answer the question about the document",
            "input_text": "Document: Insurance policy details...\nQuestion: What is covered?",
            "output": "The policy covers..."
        }
    ]
}

# Start fine-tuning
response = requests.post('http://localhost:8000/fine-tune/train', json=training_data)
result = response.json()
print(f"Model saved to: {result['model_path']}")
```

### Hybrid Search
```python
# Perform hybrid search
search_data = {
    "query": "What are the claim requirements?",
    "n_results": 3
}
response = requests.post('http://localhost:8000/hybrid/search', json=search_data)
result = response.json()
print(f"Answer: {result['answer']}")
```

## 🏗️ Architecture

### Backend Components
- **FastAPI**: Modern web framework for API
- **ChromaDB**: Vector database for document storage
- **Sentence Transformers**: Embedding generation
- **Transformers**: Fine-tuning capabilities
- **Groq**: LLM integration for text generation

### Frontend Components
- **React**: Modern UI framework
- **Tailwind CSS**: Styling
- **Lucide React**: Icons
- **Vite**: Build tool

## 🔍 Vector Database Features

### Document Storage
- Automatic text chunking with overlap
- Metadata preservation
- Persistent storage with ChromaDB
- Efficient similarity search

### Search Capabilities
- Semantic similarity search
- Configurable result count
- Distance-based relevance scoring
- Metadata filtering

## 🧠 Fine-tuning Features

### Model Training
- Support for various base models
- Custom training data preparation
- Configurable training parameters
- Model evaluation and metrics

### Training Data Format
```json
{
  "training_data": [
    {
      "instruction": "Task description",
      "input_text": "Input context",
      "output": "Expected response"
    }
  ]
}
```

## 🚀 Performance Optimization

### Vector Database
- Efficient embedding generation
- Smart text chunking
- Cosine similarity search
- Persistent storage

### Fine-tuning
- GPU acceleration support
- Configurable batch sizes
- Learning rate optimization
- Model checkpointing

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_features.py
```

This will test:
- Basic document processing
- Vector database operations
- Fine-tuning capabilities
- Hybrid search functionality

## 📊 Monitoring

### Vector Database Stats
- Total document count
- Storage location
- Collection metadata

### Fine-tuning Metrics
- Training loss
- Evaluation metrics
- Model performance

## 🔒 Security Considerations

- Input validation on all endpoints
- File type restrictions
- API key management
- Error handling and logging

## 🛠️ Development

### Adding New Features
1. Create new modules in the backend
2. Add corresponding API endpoints
3. Update frontend components
4. Add tests to `test_features.py`

### Code Structure
```
Parse_AI/
├── main.py              # FastAPI application
├── vector_db.py         # Vector database operations
├── fine_tuning.py       # Fine-tuning capabilities
├── groq_llm.py         # LLM integration
├── extract_text.py      # Text extraction
├── requirements.txt     # Dependencies
├── test_features.py     # Test suite
└── frontnd/            # React frontend
    └── src/
        ├── App.jsx      # Main app component
        └── HomePage.jsx # Feature interface
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Run the test suite
3. Review the API endpoints
4. Create an issue with detailed information

---

**Parse AI** - Advanced document intelligence with vector database and fine-tuning capabilities. 