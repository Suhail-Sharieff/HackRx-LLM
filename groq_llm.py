# import os
# from dotenv import load_dotenv

# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# from groq import Groq
# client = Groq(api_key=GROQ_API_KEY)


# def generate_summary(text: str) -> str:
#     response = client.chat.completions.create(
#         model="gemini-2.0-flash",
#         messages=[{"role": "user", "content": f"Summarize this:\n\n{text}"}],
#         max_tokens=300
#     )
#     return response.choices[0].message.content.strip()
import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GROQ_API_KEY")


# def answer_question(context: str, question: str) -> str:
#     prompt = f"""You are an AI document analyzer. Based on the documents below, answer the user's question accurately:

# Documents:
# {context}

# Question: {question}
# Answer:"""
#     response = client.chat.completions.create(
#         model="meta-llama/llama-4-scout-17b-16e-instruct",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=300,
#         temperature=0.2
#     )
#     return response.choices[0].message.content.strip()
def gemini_call(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    r = requests.post(url, headers=headers, params=params, json=data)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
def generate_summary(text: str) -> str:
    return gemini_call(f"Summarize this:\n\n{text}")
def answer_question(context: str, question: str) -> str:
    prompt = f"""You are an AI document analyzer. Based on the documents below, answer the user's question accurately:

Documents:
{context}

Question: {question}
Answer:"""
    return gemini_call(prompt)

def simulate_scenario(context: str, scenario: str) -> str:
    prompt = f"""Based on the document below, simulate the effect of this change:

Document:
{context}

Scenario:
{scenario}

Explain how the claim decision would change with this scenario."""
    return gemini_call(prompt)
# def simulate_scenario(context: str, scenario: str) -> str:
#     prompt = f"""Based on the document below, simulate the effect of this change:

# Document:
# {context}

# Scenario:
# {scenario}

# Explain how the claim decision would change with this scenario."""
#     response = client.chat.completions.create(
#         model="meta-llama/llama-4-scout-17b-16e-instruct",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=400
#     )
#     return response.choices[0].message.content.strip()
