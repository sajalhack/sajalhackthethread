#!/usr/bin/env python3
"""Test Google Gemini API connection"""

from config import GEMINI_API_KEY
import requests
import json

print("Testing Google Gemini API connection...")
print(f"API Key starts with: {GEMINI_API_KEY[:10]}...")

try:
    # Try different API versions and models
    api_versions = ["v1", "v1beta"]
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    response = None
    working_model = None
    working_version = None
    
    for api_version in api_versions:
        print(f"\n🔍 Trying API version: {api_version}")
        for model_name in models_to_try:
            print(f"  Trying model: {model_name}...")
            url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": "Say 'test' in JSON format: {\"response\": \"test\"}"
                    }]
                }]
            }
            
            try:
                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    working_model = model_name
                    working_version = api_version
                    print(f"  ✅ Model {model_name} works with {api_version}!")
                    break
                elif response.status_code == 404:
                    print(f"  ❌ Model {model_name} not found in {api_version}")
                    continue
                elif response.status_code == 403:
                    print(f"  ❌ Access denied (403) - API key may not have permissions")
                    print(f"  Response: {response.text[:200]}")
                    continue
                else:
                    print(f"  ❌ API error: {response.status_code}")
                    print(f"  Response: {response.text[:200]}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        if working_model:
            break  # Found working model, exit outer loop
    
    if working_model and response and response.status_code == 200:
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            print(f"\n✅ Google Gemini API connection successful!")
            print(f"Working API version: {working_version}")
            print(f"Working model: {working_model}")
            print(f"Response: {generated_text}")
        else:
            print("❌ Unexpected response format")
            print(f"Response: {result}")
    else:
        print("\n❌ None of the Gemini models worked.")
        print("\n💡 Troubleshooting:")
        print("1. Make sure your API key is valid")
        print("2. Enable Gemini API in Google Cloud Console:")
        print("   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
        print("3. Check API key permissions in:")
        print("   https://console.cloud.google.com/apis/credentials")
    
except Exception as e:
    print(f"❌ Gemini API error: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
