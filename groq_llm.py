import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GROQ_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# API constants
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
HEADERS = {"Content-Type": "application/json"}
PARAMS = {"key": GEMINI_API_KEY}


def gemini_call(prompt: str, max_tokens: int = 250, temperature: float = 0.2) -> str:
    """
    Sends a request to the Gemini API with optimized settings to reduce token usage.
    """
    if not prompt or not prompt.strip():
        return "Error: Empty prompt provided."

    # Truncate overly large prompts to save tokens
    prompt = prompt.strip()
    if len(prompt) > 4000:
        prompt = prompt[:4000] + "..."

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }

    try:
        r = requests.post(BASE_URL, headers=HEADERS, params=PARAMS, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return "Error: Unexpected API response format."
    except requests.RequestException as e:
        return f"Error: API request failed - {e}"


def generate_summary(text: str) -> str:
    """
    Generates a concise summary of the provided text.
    """
    if not text or not text.strip():
        return "Error: No text provided to summarize."

    # Limit text length to save tokens
    text = text.strip()[:3500]
    prompt = f"Summarize the following text clearly and concisely:\n\n{text}"
    return gemini_call(prompt, max_tokens=200)


def answer_question(context: str, question: str) -> str:
    """
    Answers a question based on the provided context.
    """
    if not context or not question:
        return "Error: Context and question are required."

    context = context.strip()[:3500]
    question = question.strip()
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer concisely and accurately:"
    return gemini_call(prompt, max_tokens=250)


def simulate_scenario(context: str, scenario: str) -> str:
    """
    Simulates how a scenario change affects the document decision.
    """
    if not context or not scenario:
        return "Error: Context and scenario are required."

    context = context.strip()[:3500]
    scenario = scenario.strip()
    prompt = f"Context:\n{context}\n\nScenario: {scenario}\nExplain the impact on the decision briefly and clearly:"
    return gemini_call(prompt, max_tokens=250)
