from groq import Groq

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
    # Extract content and check if it contains code block
    content = completion.choices[0].message.content

    # Look for code block delimiters
    start_delimiter = "```"
    end_delimiter = "```"
    
    # Find start and end positions of code block
    start_pos = content.find(start_delimiter) + len(start_delimiter)
    end_pos = content.rfind(end_delimiter)
    
    # Extract code between delimiters if found, otherwise return full content
    if start_pos > len(start_delimiter) and end_pos > start_pos:
        # Skip the language identifier (e.g., 'cpp\n') if present
        code_start = content.find('\n', start_pos) + 1
        if code_start > start_pos and code_start < end_pos:
            print(content[code_start:end_pos].strip())
        else:
            print(content[start_pos:end_pos].strip())
    else:
        print(content)
except Exception as e:
    print(f"Error: Failed to execute request. {str(e)}")
