# Architecture Diagram

## System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        USER (WhatsApp)                        │
│                    Sends Instagram Link                        │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    TWILIO WHATSAPP API                       │
│              Receives message via webhook                     │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                         │
│                    (app.py - /webhook)                        │
└───────────────────────────┬───────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Extract    │   │   Extract    │   │   Extract    │
│  Instagram   │   │   Twitter    │   │   Article    │
│   Content    │   │   Content    │   │   Content    │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   Content Data        │
              │  (caption, hashtags)  │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    AI PROCESSING      │
              │  (Keyword Matching)   │
              │                       │
              │  • Auto-tagging       │
              │  • Summarization      │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   SQLite DATABASE      │
              │     (saves.db)         │
              │                        │
              │  Stores:               │
              │  • URL                 │
              │  • Platform            │
              │  • Caption             │
              │  • Hashtags            │
              │  • Category            │
              │  • Summary             │
              │  • Timestamp           │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   DASHBOARD API        │
              │  (/api/saves)          │
              │  (/api/random)         │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   WEB DASHBOARD        │
              │  (dashboard.html)      │
              │                        │
              │  Features:            │
              │  • Card Layout            │
              │  • Search              │
              │  • Instagram Embeds    │
              │  • Random Inspiration  │
              └───────────────────────┘
```

## Component Details

### 1. WhatsApp Input Layer
- **Twilio Sandbox**: Receives WhatsApp messages
- **Webhook Endpoint**: `/webhook` in Flask app
- **Message Processing**: Extracts URLs from incoming messages

### 2. Content Extraction Layer
- **Instagram**: Extracts caption and hashtags from Instagram URLs
- **Twitter**: Extracts tweet content and hashtags
- **Articles**: Extracts title and main text from blog posts

### 3. AI Processing Layer
- **Enhanced Keyword-Based System**: 
  - Score-based categorization across 10+ categories
  - Intelligent keyword matching
  - Automatic summary generation from captions
- **Fallback Support**: Works reliably without external APIs

### 4. Data Storage Layer
- **SQLite Database**: Lightweight, file-based database
- **Schema**: Stores all extracted and processed content
- **Indexing**: Enables fast search queries

### 5. Presentation Layer
- **RESTful API**: Provides data to frontend
- **Dashboard**: Modern, responsive web interface
- **Search**: Real-time filtering across all fields
- **Embeds**: Instagram post embeds when available

## Data Flow Example

1. User sends: `https://instagram.com/p/xyz123` via WhatsApp
2. Twilio forwards to Flask `/webhook` endpoint
3. Flask extracts Instagram content (caption, hashtags)
4. AI processes: Category = "Fitness", Summary = "Great abs workout..."
5. Data saved to SQLite database
6. Bot responds: "✅ Got it! Saved to your 'Fitness' bucket."
7. User visits dashboard, sees new card with embedded Instagram post

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **WhatsApp API**: Twilio
- **AI Processing**: Enhanced keyword-based system
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: ngrok (for local testing)

## API Endpoints

- `GET /` - Dashboard homepage
- `GET /api/saves?search=query` - Get all saves (optionally filtered)
- `GET /api/random` - Get a random save
- `GET /health` - Health check endpoint
- `POST /webhook` - Twilio webhook for WhatsApp messages
