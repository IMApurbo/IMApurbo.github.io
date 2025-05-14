#!/bin/bash

# Define the API endpoint and output file
URL="https://api.groq.com/openai/v1/chat/completions"
OUTPUT_FILE="response.json"
API_KEY="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"

# Prompt user for input
echo "Enter your prompt (e.g., Explain the importance of fast language models):"
read -r USER_PROMPT

# Escape double quotes in the user input to ensure valid JSON
ESCAPED_PROMPT=$(echo "$USER_PROMPT" | sed 's/"/\\"/g')

# Run the curl command with user input
curl -X POST "$URL" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d "{\"messages\":[{\"role\":\"user\",\"content\":\"$ESCAPED_PROMPT\"}],\"model\":\"Llama-3.3-70B-Versatile\"}" \
     -o "$OUTPUT_FILE"

# Check if curl was successful
if [ $? -eq 0 ]; then
    echo "Successfully saved response to $OUTPUT_FILE"
else
    echo "Error: Failed to execute curl command"
    exit 1
fi
