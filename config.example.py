# Configuration file template
# Copy this file to config.py and add your actual API keys
# DO NOT commit config.py to git!

# AI Configuration - Choose one:
# Option 1: OpenAI (requires paid credits)
OPENAI_API_KEY = "your_openai_api_key_here"

# Option 2: Hugging Face (FREE - no API key needed for public models!)
# Get free token at: https://huggingface.co/settings/tokens
HUGGINGFACE_API_TOKEN = ""  # Optional - only needed for private models

# Option 3: Google Gemini (FREE tier available)
# Get free API key at: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "your_gemini_api_key_here"

# Twilio Configuration
TWILIO_ACCOUNT_SID = "your_twilio_account_sid_here"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token_here"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# AI Provider Selection: "openai", "huggingface", "gemini", or "fallback"
AI_PROVIDER = "fallback"  # Using enhanced keyword-based system (FREE & RELIABLE!)
