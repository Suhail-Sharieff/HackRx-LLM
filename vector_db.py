# vector_db.py
import chromadb
from sentence_transformers import SentenceTransformer
import uuid
import re
from typing import List, Dict, Any

def smart_text_splitter(text: str, chunk_size: int) -> List[str]:
    if len(text) <= chunk_size:
        return [text]
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    all_chunks = []
    for para in paragraphs:
        if len(para) <= chunk_size:
            all_chunks.append(para)
        else:
            sentences = re.split(r'(?<=[.!?])\s+', para)
            current_chunk = ""
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 <= chunk_size:
                    current_chunk += sentence + " "
                else:
                    all_chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
            if current_chunk:
                all_chunks.append(current_chunk.strip())
    return [chunk for chunk in all_chunks if chunk]

class VectorDatabase:
    def __init__(self):
        self.client = chromadb.Client()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2') # Fastest model
        self.chunk_size = 800
        self.collection = self.client.get_or_create_collection(name="documents", metadata={"hnsw:space": "cosine"})

    def add_document(self, text: str, metadata: Dict[str, Any]):
        chunks = smart_text_splitter(text, self.chunk_size)
        if not chunks: return
        embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [metadata.copy() for _ in chunks]
        self.collection.add(embeddings=embeddings.tolist(), documents=chunks, metadatas=metadatas, ids=ids)

    def search_similar(self, query: str, n_results: int = 4) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_model.encode([query])
        results = self.collection.query(query_embeddings=query_embedding.tolist(), n_results=n_results, include=['documents'])
        formatted_results = []
        if results and results.get('documents') and results['documents'][0]:
            for doc in results['documents'][0]:
                formatted_results.append({'document': doc})
        return formatted_results