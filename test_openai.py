#!/usr/bin/env python3
"""Test OpenAI API connection"""

from config import OPENAI_API_KEY
import openai

print("Testing OpenAI API connection...")
print(f"API Key starts with: {OPENAI_API_KEY[:10]}...")

try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'test' in JSON format: {\"response\": \"test\"}"}
        ],
        max_tokens=20
    )
    
    print("✅ OpenAI API connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI API error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
