from groq import Groq
import json

# Initialize Groq client with API key
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Default prompt
DEFAULT_PROMPT = "Explain the importance of fast language models"

# Get user input with default prompt option
user_prompt = input(f"Enter your prompt (press Enter for default: '{DEFAULT_PROMPT}'): ") or DEFAULT_PROMPT

# Create chat completion
try:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": user_prompt}]
    )
    print("Response received successfully:")
    print(json.dumps(completion.to_dict(), indent=2))
except Exception as e:
    print(f"Error: Failed to execute request. {str(e)}")
