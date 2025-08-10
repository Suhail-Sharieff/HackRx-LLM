# groq_llm.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client with your new Groq key
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    raise ValueError("Groq API Key not found or is invalid. Please check your .env file.") from e

def gemini_call(prompt: str) -> str:
    """
    Sends a request to the Groq API to use the Gemma model.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192", # Using the Gemma model hosted by Groq
            temperature=0.2,
            max_tokens=300,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # This will now catch errors from the Groq API
        print(f"An error occurred with the Groq API call: {e}")
        # Let the exception bubble up so the retry logic in main.py can handle it
        raise e