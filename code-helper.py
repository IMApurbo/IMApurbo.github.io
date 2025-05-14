import requests
import json

# Define the API endpoint and API key
URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = "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"

# Default prompt
DEFAULT_PROMPT = "Explain the importance of fast language models"

# Get user input with default prompt option
user_prompt = input(f"Enter your prompt (press Enter for default: '{DEFAULT_PROMPT}'): ") or DEFAULT_PROMPT

# Prepare headers and payload
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "messages": [{"role": "user", "content": user_prompt}],
    "model": "Llama-3.3-70B-Versatile"
}

# Make the API request
response = requests.post(URL, headers=headers, json=payload)

# Check if request was successful
if response.status_code == 200:
    print("Response received successfully:")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: Failed to execute request. Status code: {response.status_code}")
