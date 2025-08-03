import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os
from typing import List, Dict, Any, Optional
import uuid

class VectorDatabase:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize vector database with ChromaDB and sentence transformers"""
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize sentence transformer model for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_document(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """Add a document to the vector database"""
        # Split text into chunks for better retrieval
        chunks = self._split_text(text, chunk_size=1000, overlap=200)
        
        # Generate embeddings for chunks
        embeddings = self.embedding_model.encode(chunks)
        
        # Prepare documents for insertion
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [metadata or {} for _ in chunks] if metadata else [{} for _ in chunks]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        return ids[0]  # Return first chunk ID as document ID
    
    def search_similar(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted_results
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific document by ID"""
        try:
            result = self.collection.get(ids=[doc_id])
            if result['documents']:
                return {
                    'document': result['documents'][0],
                    'metadata': result['metadatas'][0] if result['metadatas'] else {}
                }
        except Exception as e:
            print(f"Error retrieving document: {e}")
        return None
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the database"""
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from the database"""
        try:
            result = self.collection.get()
            documents = []
            for i in range(len(result['documents'])):
                documents.append({
                    'id': result['ids'][i],
                    'document': result['documents'][i],
                    'metadata': result['metadatas'][i] if result['metadatas'] else {}
                })
            return documents
        except Exception as e:
            print(f"Error retrieving all documents: {e}")
            return []
    
    def _split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # If not the last chunk, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'persist_directory': self.persist_directory
            }
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {'total_documents': 0, 'persist_directory': self.persist_directory}

# Global instance
vector_db = VectorDatabase() 