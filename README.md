# 📄 HackRx – Parse AI

A modern web application that uses **Groq's LLM** to process insurance claim documents (PDFs/images), extract summaries, answer user queries, simulate policy scenarios, and explain reasoning chains for claim approval or rejection.

## 🚀 Features

- 🔍 **Document Parsing** – Upload PDFs or images, extract text using OCR/PyPDF2
- 🧠 **LLM Summarization** – Generate concise summaries from full policy/claim docs
- ❓ **Ask Questions** – Ask natural language questions about document contents
- 🎛️ **Scenario Simulation** – Modify "what-if" conditions and see outcome changes
- 📊 **Explainable Decision Chains** – Trace decisions step-by-step using clauses
- 🛡 **Clause Conflict Detection** – Flag contradictory or overlapping rules
- 🗂 **Bulk Upload (Future)** – Process ZIPs and categorize metadata using embeddings
- 🎨 **Modern React Frontend** – Beautiful, responsive UI with drag-and-drop upload

## 🧑‍💻 Tech Stack

| Frontend           | Backend          | AI/LLM             | Other Tools        |
|--------------------|------------------|--------------------|--------------------|
| React + TypeScript | FastAPI (Python) | Groq (Meta-Llama)  | Tesseract, PyPDF2  |
| Tailwind CSS       | Uvicorn          | Natural Language QA| PIL, Pydantic      |
| Lucide React Icons |                  |                    |                    |

---

## ⚙️ Getting Started

### 🔧 Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Start backend server
python main.py
```

### 🎨 Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 🚀 Quick Start (Both Frontend & Backend)

```bash
# Install frontend dependencies
npm run setup

# Start both frontend and backend
npm run dev
```

This will start:
- Backend API server on `http://localhost:8000`
- React frontend on `http://localhost:3000`

## 📦 API Endpoints

| Method | Endpoint     | Description                                |
|--------|--------------|--------------------------------------------|
| POST   | `/upload`    | Upload and process a document              |
| POST   | `/query`     | Ask a question about a document            |
| GET    | `/documents` | List all processed documents               |
| DELETE | `/documents/{doc_id}` | Delete a document                    |

## 🎯 Frontend Features

- **📄 Document Upload**: Drag-and-drop interface for PDF/DOCX files
- **📚 Document Management**: View, select, and delete uploaded documents
- **💬 AI Chat Interface**: Real-time Q&A with your documents
- **🎨 Modern UI**: Clean, responsive design with Tailwind CSS
- **⚡ Real-time Updates**: Instant feedback and loading states

## 📁 Project Structure

```
Parse_AI/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── types/          # TypeScript types
│   ├── package.json
│   └── README.md
├── main.py                  # FastAPI backend server
├── requirements.txt         # Python dependencies
├── package.json            # Root package.json for scripts
└── README.md              # This file
```

## 🔧 Development

### Backend Development
```bash
# Start backend with auto-reload
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm start
```

### Running Both
```bash
npm run dev
```

## 🚀 Deployment

### Frontend Build
```bash
cd frontend
npm run build
```

### Backend Deployment
The FastAPI backend can be deployed using:
- Docker
- Heroku
- Railway
- Any Python hosting platform

## 📝 License

This project is licensed under the MIT License.


