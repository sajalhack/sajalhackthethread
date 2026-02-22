from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import openai
import sqlite3
import re
from datetime import datetime
import json

load_dotenv()

# Import config with all credentials
try:
    from config import (OPENAI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, 
                       TWILIO_WHATSAPP_NUMBER, HUGGINGFACE_API_TOKEN, 
                       GEMINI_API_KEY, AI_PROVIDER)
except ImportError:
    # Fallback to environment variables
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'huggingface')  # Default to free option

# Override with .env if it exists (takes priority)
if os.getenv('OPENAI_API_KEY'):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if os.getenv('TWILIO_ACCOUNT_SID'):
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
if os.getenv('TWILIO_AUTH_TOKEN'):
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
if os.getenv('TWILIO_WHATSAPP_NUMBER'):
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
if os.getenv('HUGGINGFACE_API_TOKEN'):
    HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
if os.getenv('GEMINI_API_KEY'):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if os.getenv('AI_PROVIDER'):
    AI_PROVIDER = os.getenv('AI_PROVIDER')

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Allow ngrok and localhost
app.config['SERVER_NAME'] = None

openai.api_key = OPENAI_API_KEY

# Database setup
def init_db():
    conn = sqlite3.connect('saves.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS saves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            platform TEXT,
            caption TEXT,
            hashtags TEXT,
            category TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def extract_instagram_content(url):
    """Extract caption and hashtags from Instagram URL"""
    try:
        # Instagram doesn't allow direct scraping, so we'll use a workaround
        # For demo purposes, we'll extract what we can from the URL structure
        # In production, you'd need Instagram Basic Display API or similar
        
        # Try to get page content (may be blocked, but worth trying)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        caption = ""
        hashtags = []
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find meta tags with description
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                caption = meta_desc.get('content', '')
            
            # Extract hashtags from caption
            hashtag_pattern = r'#(\w+)'
            hashtags = re.findall(hashtag_pattern, caption)
        
        # If we couldn't extract, return defaults
        if not caption:
            caption = "Instagram content saved"
        
        return {
            'caption': caption,
            'hashtags': hashtags,
            'platform': 'instagram'
        }
    except Exception as e:
        print(f"Error extracting Instagram content: {e}")
        return {
            'caption': "Instagram content saved",
            'hashtags': [],
            'platform': 'instagram'
        }

def extract_twitter_content(url):
    """Extract content from Twitter/X URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        caption = ""
        hashtags = []
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find meta tags
            meta_desc = soup.find('meta', property='og:description')
            if meta_desc:
                caption = meta_desc.get('content', '')
            
            # Extract hashtags
            hashtag_pattern = r'#(\w+)'
            hashtags = re.findall(hashtag_pattern, caption)
        
        if not caption:
            caption = "Twitter content saved"
        
        return {
            'caption': caption,
            'hashtags': hashtags,
            'platform': 'twitter'
        }
    except Exception as e:
        print(f"Error extracting Twitter content: {e}")
        return {
            'caption': "Twitter content saved",
            'hashtags': [],
            'platform': 'twitter'
        }

def extract_article_content(url):
    """Extract title and main text from article/blog"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get title
            title = ""
            if soup.title:
                title = soup.title.string
            else:
                og_title = soup.find('meta', property='og:title')
                if og_title:
                    title = og_title.get('content', '')
            
            # Get main content (try article tag, or main, or just p tags)
            content = ""
            article = soup.find('article')
            if article:
                content = article.get_text(strip=True, separator=' ')
            else:
                main = soup.find('main')
                if main:
                    content = main.get_text(strip=True, separator=' ')
                else:
                    # Get all paragraphs
                    paragraphs = soup.find_all('p')
                    content = ' '.join([p.get_text(strip=True) for p in paragraphs[:10]])
            
            # Limit content length
            if len(content) > 1000:
                content = content[:1000] + "..."
            
            caption = f"{title}\n\n{content}" if title else content
            
            return {
                'caption': caption,
                'hashtags': [],
                'platform': 'article'
            }
    except Exception as e:
        print(f"Error extracting article content: {e}")
    
    return {
        'caption': "Article content saved",
        'hashtags': [],
        'platform': 'article'
    }

def extract_content(url):
    """Determine platform and extract content accordingly"""
    if 'instagram.com' in url:
        return extract_instagram_content(url)
    elif 'twitter.com' in url or 'x.com' in url:
        return extract_twitter_content(url)
    else:
        return extract_article_content(url)

def ai_tag_and_summarize_huggingface(caption, hashtags):
    """Use Hugging Face Inference API (FREE!)"""
    try:
        hashtags_str = ', '.join(hashtags) if hashtags else 'none'
        if not caption or len(caption.strip()) < 5:
            caption = "Social media content"
        
        prompt = f"""Analyze this social media content and provide:
1. A category (choose ONE from: Fitness, Coding, Food, Travel, Design, Fashion, Music, Photography, Business, Education, Other)
2. A one-sentence summary

Content: {caption}
Hashtags: {hashtags_str}

Respond in JSON format:
{{
    "category": "category_name",
    "summary": "one sentence summary"
}}"""

        # Use Hugging Face Inference API (free, no API key needed for public models)
        api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        # Try a better model for text generation
        headers = {}
        if HUGGINGFACE_API_TOKEN:
            headers["Authorization"] = f"Bearer {HUGGINGFACE_API_TOKEN}"
        
        # Use a simpler approach - use Hugging Face's text generation API
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        # Try using a text generation model
        response = requests.post(
            "https://api-inference.huggingface.co/models/gpt2",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Try to extract JSON from response
                if '{' in generated_text and '}' in generated_text:
                    start = generated_text.find('{')
                    end = generated_text.rfind('}') + 1
                    json_str = generated_text[start:end]
                    data = json.loads(json_str)
                    category = data.get('category', 'Other')
                    summary = data.get('summary', 'Content saved')
                    return category, summary
        
        # If Hugging Face fails, fall through to fallback
        raise Exception("Hugging Face API returned unexpected response")
    
    except Exception as e:
        print(f"Hugging Face API error: {e}")
        raise  # Re-raise to trigger fallback

def ai_tag_and_summarize_gemini(caption, hashtags):
    """Use Google Gemini API (FREE tier available)"""
    try:
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
        
        hashtags_str = ', '.join(hashtags) if hashtags else 'none'
        if not caption or len(caption.strip()) < 5:
            caption = "Social media content"
        
        prompt = f"""Analyze this social media content and provide:
1. A category (choose ONE from: Fitness, Coding, Food, Travel, Design, Fashion, Music, Photography, Business, Education, Other)
2. A one-sentence summary

Content: {caption}
Hashtags: {hashtags_str}

Respond in JSON format:
{{
    "category": "category_name",
    "summary": "one sentence summary"
}}"""

        # Use Google Gemini API - try different API versions and models
        # Try v1 API first (newer), then v1beta
        api_versions = ["v1", "v1beta"]
        models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        
        response = None
        for api_version in api_versions:
            for model_name in models_to_try:
                try:
                    url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
                    payload = {
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                    
                    response = requests.post(url, json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        print(f"✅ Using Gemini {api_version}/{model_name}")
                        break  # Success, use this model
                    elif response.status_code == 404:
                        print(f"❌ Model {model_name} not found in {api_version}, trying next...")
                        continue  # Try next model
                    else:
                        print(f"❌ API error {response.status_code}: {response.text[:200]}")
                        response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        continue  # Try next model
                    print(f"❌ HTTP Error: {e}")
                    raise
                except Exception as e:
                    print(f"❌ Error trying {api_version}/{model_name}: {e}")
                    continue
            
            if response and response.status_code == 200:
                break  # Found working model, exit outer loop
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                
                # Extract JSON
                if '{' in generated_text and '}' in generated_text:
                    start = generated_text.find('{')
                    end = generated_text.rfind('}') + 1
                    json_str = generated_text[start:end]
                    data = json.loads(json_str)
                    category = data.get('category', 'Other')
                    summary = data.get('summary', 'Content saved')
                    return category, summary
            else:
                raise Exception("No candidates in Gemini response")
        else:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"Gemini API error: {e}")
        raise  # Re-raise to trigger fallback

def ai_tag_and_summarize_openai(caption, hashtags):
    """Use OpenAI API"""
    try:
        if not OPENAI_API_KEY or OPENAI_API_KEY == 'your_openai_api_key_here':
            raise ValueError("OpenAI API key not configured")
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        hashtags_str = ', '.join(hashtags) if hashtags else 'none'
        if not caption or len(caption.strip()) < 5:
            caption = "Social media content"
        
        prompt = f"""Analyze this social media content and provide:
1. A category (choose ONE from: Fitness, Coding, Food, Travel, Design, Fashion, Music, Photography, Business, Education, Other)
2. A one-sentence summary

Content: {caption}
Hashtags: {hashtags_str}

Respond in JSON format:
{{
    "category": "category_name",
    "summary": "one sentence summary"
}}"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that categorizes and summarizes social media content. Always respond with valid JSON only, no markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        result = response.choices[0].message.content.strip()
        
        # Try to parse JSON
        if result.startswith('```'):
            result = result.split('```')[1]
            if result.startswith('json'):
                result = result[4:]
            result = result.strip()
        
        if '{' in result and '}' in result:
            start = result.find('{')
            end = result.rfind('}') + 1
            result = result[start:end]
        
        data = json.loads(result)
        category = data.get('category', 'Other')
        summary = data.get('summary', 'Content saved')
        
        valid_categories = ['Fitness', 'Coding', 'Food', 'Travel', 'Design', 'Fashion', 'Music', 'Photography', 'Business', 'Education', 'Other']
        if category not in valid_categories:
            category = 'Other'
        
        return category, summary
    
    except openai.RateLimitError as e:
        print(f"OpenAI API quota exceeded: {e}")
        raise
    except Exception as e:
        print(f"OpenAI API error: {e}")
        raise

def ai_tag_and_summarize(caption, hashtags):
    """Main AI function - tries different providers based on config"""
    # Determine which provider to use
    try:
        provider = AI_PROVIDER if 'AI_PROVIDER' in globals() else 'fallback'
    except:
        provider = 'fallback'
    
    # Try the selected provider
    if provider == 'huggingface':
        try:
            return ai_tag_and_summarize_huggingface(caption, hashtags)
        except Exception as e:
            print(f"Hugging Face failed: {e}, trying fallback...")
    elif provider == 'gemini' and GEMINI_API_KEY:
        try:
            return ai_tag_and_summarize_gemini(caption, hashtags)
        except Exception as e:
            print(f"Gemini failed: {e}, trying fallback...")
    elif provider == 'openai' and OPENAI_API_KEY and OPENAI_API_KEY != 'your_openai_api_key_here':
        try:
            return ai_tag_and_summarize_openai(caption, hashtags)
        except Exception as e:
            print(f"OpenAI failed: {e}, trying fallback...")
    
    # All AI providers failed or not configured - use ENHANCED fallback
    
    # Enhanced intelligent fallback categorization
    caption_lower = (caption or "").lower()
    hashtags_lower = [h.lower() for h in (hashtags or [])]
    all_text = caption_lower + " " + " ".join(hashtags_lower)
    
    # Score-based categorization (more accurate)
    category_scores = {
        'Fitness': ['workout', 'fitness', 'exercise', 'gym', 'abs', 'cardio', 'yoga', 'pilates', 'running', 'training', 'muscle', 'strength', 'health', 'fit', 'diet', 'weight', 'nutrition'],
        'Coding': ['code', 'programming', 'developer', 'python', 'javascript', 'coding', 'tutorial', 'algorithm', 'software', 'tech', 'coding', 'webdev', 'app', 'api', 'github', 'stackoverflow'],
        'Food': ['recipe', 'food', 'cooking', 'pasta', 'meal', 'dish', 'cuisine', 'chef', 'baking', 'restaurant', 'delicious', 'tasty', 'recipe', 'cook', 'kitchen', 'dinner', 'lunch', 'breakfast'],
        'Travel': ['travel', 'trip', 'vacation', 'destination', 'traveling', 'adventure', 'wanderlust', 'explore', 'journey', 'vacation', 'holiday', 'tourism', 'visit', 'sightseeing'],
        'Design': ['design', 'graphic', 'ui', 'ux', 'art', 'creative', 'illustration', 'logo', 'branding', 'aesthetic', 'visual', 'typography', 'layout'],
        'Fashion': ['fashion', 'style', 'outfit', 'clothing', 'wardrobe', 'trend', 'fashionable', 'dress', 'accessories', 'style'],
        'Music': ['music', 'song', 'artist', 'album', 'concert', 'musician', 'beat', 'lyrics', 'spotify', 'playlist'],
        'Photography': ['photo', 'photography', 'camera', 'shot', 'picture', 'image', 'photographer', 'lens', 'portrait', 'landscape'],
        'Business': ['business', 'entrepreneur', 'startup', 'marketing', 'sales', 'strategy', 'finance', 'investment', 'company'],
        'Education': ['learn', 'education', 'study', 'course', 'tutorial', 'lesson', 'student', 'school', 'university', 'knowledge']
    }
    
    scores = {}
    for category, keywords in category_scores.items():
        score = sum(1 for keyword in keywords if keyword in all_text)
        if score > 0:
            scores[category] = score
    
    # Get category with highest score
    if scores:
        category = max(scores, key=scores.get)
    else:
        category = 'Other'
    
    # Create intelligent summary from caption
    if caption and len(caption.strip()) > 10:
        # Try to create a meaningful summary
        sentences = caption.split('.')
        if len(sentences) > 1:
            # Use first sentence as summary
            summary = sentences[0].strip()
            if len(summary) > 150:
                summary = summary[:147] + "..."
        else:
            # Use first part of caption
            summary = caption[:150].strip()
            if len(caption) > 150:
                summary += "..."
    else:
        # Create summary from category and hashtags
        if hashtags:
            summary = f"{category} content: {', '.join(hashtags[:3])}"
        else:
            summary = f"{category} content saved"
    
    return category, summary

def save_to_db(url, platform, caption, hashtags, category, summary):
    """Save content to database"""
    conn = sqlite3.connect('saves.db')
    c = conn.cursor()
    hashtags_str = ', '.join(hashtags) if hashtags else ''
    c.execute('''
        INSERT INTO saves (url, platform, caption, hashtags, category, summary)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (url, platform, caption, hashtags_str, category, summary))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Dashboard homepage"""
    return render_template('dashboard.html')

@app.route('/api/saves', methods=['GET'])
def get_saves():
    """Get all saves, optionally filtered by search query"""
    search = request.args.get('search', '').lower()
    
    conn = sqlite3.connect('saves.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if search:
        c.execute('''
            SELECT * FROM saves 
            WHERE LOWER(caption) LIKE ? OR LOWER(category) LIKE ? OR LOWER(hashtags) LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{search}%', f'%{search}%', f'%{search}%'))
    else:
        c.execute('SELECT * FROM saves ORDER BY created_at DESC')
    
    rows = c.fetchall()
    saves = [dict(row) for row in rows]
    conn.close()
    
    return jsonify(saves)

@app.route('/api/random', methods=['GET'])
def get_random():
    """Get a random save for inspiration"""
    conn = sqlite3.connect('saves.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM saves ORDER BY RANDOM() LIMIT 1')
    row = c.fetchone()
    conn.close()
    
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'No saves found'}), 404

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Twilio webhook handler for WhatsApp messages"""
    # Handle GET requests (for testing)
    if request.method == 'GET':
        return jsonify({
            'status': 'ok',
            'message': 'Webhook endpoint is active',
            'method': 'GET'
        }), 200
    
    # Handle POST requests from Twilio
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    
    # Check if message contains a URL
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, incoming_msg)
    
    if not urls:
        resp = MessagingResponse()
        resp.message("👋 Hi! Send me an Instagram, Twitter, or article link and I'll save it to your dashboard!")
        return str(resp)
    
    # Process the first URL found
    url = urls[0]
    
    try:
        # Extract content
        content_data = extract_content(url)
        caption = content_data['caption']
        hashtags = content_data['hashtags']
        platform = content_data['platform']
        
        # AI processing
        try:
            category, summary = ai_tag_and_summarize(caption, hashtags)
        except Exception as e:
            print(f"Error in AI processing: {e}")
            # Use fallback
            category = 'Other'
            summary = caption[:100] + "..." if len(caption) > 100 else (caption or "Content saved")
        
        # Ensure we have valid values
        if not category:
            category = 'Other'
        if not summary or summary == "Could not summarize":
            summary = caption[:100] + "..." if caption and len(caption) > 10 else "Content saved successfully"
        
        # Save to database
        save_to_db(url, platform, caption, hashtags, category, summary)
        
        # Respond to user
        resp = MessagingResponse()
        resp.message(f"✅ Got it! Saved to your '{category}' bucket.\n\n📝 {summary}\n\nView at: {request.host_url}")
        return str(resp)
    
    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()
        resp = MessagingResponse()
        # Still save the link even if processing fails
        try:
            save_to_db(url, 'unknown', url, [], 'Other', 'Link saved')
            resp.message(f"✅ Link saved! (Processing had issues: {str(e)[:50]})")
        except:
            resp.message(f"❌ Oops! Something went wrong. Error: {str(e)[:100]}")
        return str(resp)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

if __name__ == '__main__':
    # Allow connections from all hosts (needed for ngrok)
    # Using port 5002 as requested
    app.run(debug=True, port=5002, host='0.0.0.0')
