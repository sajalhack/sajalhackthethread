#!/usr/bin/env python3
"""
Simple test script to verify your Social Saver Bot setup.
Run this after installing dependencies and setting up .env file.
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    try:
        import flask
        print("  ✅ Flask")
    except ImportError:
        print("  ❌ Flask - Run: pip install flask")
        return False
    
    try:
        import twilio
        print("  ✅ Twilio")
    except ImportError:
        print("  ❌ Twilio - Run: pip install twilio")
        return False
    
    try:
        import openai
        print("  ✅ OpenAI")
    except ImportError:
        print("  ❌ OpenAI - Run: pip install openai")
        return False
    
    try:
        import requests
        print("  ✅ Requests")
    except ImportError:
        print("  ❌ Requests - Run: pip install requests")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  ✅ BeautifulSoup4")
    except ImportError:
        print("  ❌ BeautifulSoup4 - Run: pip install beautifulsoup4")
        return False
    
    try:
        import sqlite3
        print("  ✅ SQLite3 (built-in)")
    except ImportError:
        print("  ❌ SQLite3")
        return False
    
    return True

def test_env_vars():
    """Test if environment variables are set"""
    print("\n🔍 Testing environment variables...")
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("  ❌ OPENAI_API_KEY not set in .env")
        return False
    else:
        print(f"  ✅ OPENAI_API_KEY set (starts with: {openai_key[:7]}...)")
    
    if not twilio_sid or twilio_sid == 'your_twilio_account_sid_here':
        print("  ❌ TWILIO_ACCOUNT_SID not set in .env")
        return False
    else:
        print(f"  ✅ TWILIO_ACCOUNT_SID set (starts with: {twilio_sid[:2]}...)")
    
    if not twilio_token or twilio_token == 'your_twilio_auth_token_here':
        print("  ❌ TWILIO_AUTH_TOKEN not set in .env")
        return False
    else:
        print(f"  ✅ TWILIO_AUTH_TOKEN set")
    
    return True

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔍 Testing OpenAI API connection...")
    load_dotenv()
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("  ⚠️  Skipping - OPENAI_API_KEY not set")
        return True
    
    try:
        import openai
        client = openai.OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'test'"}],
            max_tokens=5
        )
        print("  ✅ OpenAI API connection successful")
        return True
    except Exception as e:
        print(f"  ❌ OpenAI API error: {str(e)}")
        return False

def test_database():
    """Test database creation"""
    print("\n🔍 Testing database...")
    try:
        import sqlite3
        conn = sqlite3.connect('saves.db')
        c = conn.cursor()
        c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="saves"')
        if c.fetchone():
            print("  ✅ Database table 'saves' exists")
        else:
            print("  ⚠️  Database table doesn't exist (will be created on first run)")
        conn.close()
        return True
    except Exception as e:
        print(f"  ❌ Database error: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("Social Saver Bot - Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_env_vars():
        all_passed = False
    
    if not test_database():
        all_passed = False
    
    # Only test OpenAI if key is set
    load_dotenv()
    if os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here':
        if not test_openai_connection():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed! You're ready to run the app.")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. In another terminal: ngrok http 5000")
        print("3. Configure Twilio webhook with ngrok URL")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    print("=" * 50)

if __name__ == '__main__':
    main()
