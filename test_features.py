#!/usr/bin/env python3
"""
Test script for Parse AI features including vector database and fine-tuning
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
API_BASE = "http://127.0.0.1:8000"

def test_vector_database():
    """Test vector database functionality"""
    print("🔍 Testing Vector Database Features...")
    
    # Test vector search
    search_data = {
        "query": "insurance claim",
        "n_results": 3
    }
    
    try:
        response = requests.post(f"{API_BASE}/vector/search", json=search_data)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Vector search successful: {results['total_found']} results found")
        else:
            print(f"❌ Vector search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Vector search error: {e}")
    
    # Test vector stats
    try:
        response = requests.get(f"{API_BASE}/vector/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Vector stats retrieved: {stats['total_documents']} documents")
        else:
            print(f"❌ Vector stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Vector stats error: {e}")

def test_fine_tuning():
    """Test fine-tuning functionality"""
    print("\n🧠 Testing Fine-tuning Features...")
    
    # Test fine-tune generation (will fail if no model loaded, which is expected)
    try:
        response = requests.get(f"{API_BASE}/fine-tune/generate?prompt=Hello&max_length=50")
        if response.status_code == 400:
            print("✅ Fine-tune generation correctly reports no model loaded (expected)")
        else:
            print(f"❌ Fine-tune generation unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Fine-tune generation error: {e}")

def test_hybrid_search():
    """Test hybrid search functionality"""
    print("\n🔗 Testing Hybrid Search...")
    
    search_data = {
        "query": "document analysis",
        "n_results": 2
    }
    
    try:
        response = requests.post(f"{API_BASE}/hybrid/search", json=search_data)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Hybrid search successful: {len(results['vector_results'])} vector results")
            print(f"   Answer: {results['answer'][:100]}...")
        else:
            print(f"❌ Hybrid search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Hybrid search error: {e}")

def test_basic_features():
    """Test basic document processing features"""
    print("\n📄 Testing Basic Features...")
    
    # Test ask question
    ask_data = {
        "context": "This is a test document about insurance claims processing.",
        "question": "What is this document about?"
    }
    
    try:
        response = requests.post(f"{API_BASE}/ask", json=ask_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ask question successful: {result['answer'][:50]}...")
        else:
            print(f"❌ Ask question failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Ask question error: {e}")
    
    # Test simulation
    sim_data = {
        "context": "Insurance claim for car accident with $5000 damage.",
        "scenario": "What if the damage was $10000 instead?"
    }
    
    try:
        response = requests.post(f"{API_BASE}/simulate", json=sim_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Simulation successful: {result['result'][:50]}...")
        else:
            print(f"❌ Simulation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Simulation error: {e}")

def check_server_status():
    """Check if the server is running"""
    print("🚀 Checking server status...")
    
    try:
        response = requests.get(f"{API_BASE}/docs")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Server check error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Parse AI Feature Test Suite")
    print("=" * 50)
    
    # Check server status first
    if not check_server_status():
        return
    
    # Run tests
    test_basic_features()
    test_vector_database()
    test_fine_tuning()
    test_hybrid_search()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("\n📋 Feature Summary:")
    print("• Document upload with vector storage")
    print("• Q&A with context")
    print("• Scenario simulation")
    print("• Vector database search")
    print("• Fine-tuning capabilities")
    print("• Hybrid search (vector + LLM)")
    print("• RESTful API endpoints")

if __name__ == "__main__":
    main() 