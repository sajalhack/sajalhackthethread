# Social Saver Bot 🤖📚

A WhatsApp bot that turns your Instagram saves (and other social media links) into a searchable knowledge base.

## 🎯 Features

- **WhatsApp Integration**: Send Instagram, Twitter, or article links via WhatsApp
- **AI-Powered Categorization**: Automatically tags content (Fitness, Coding, Food, Travel, etc.)
- **Smart Summarization**: Generates one-sentence summaries using OpenAI
- **Beautiful Dashboard**: Clean, searchable web interface to browse your saves
- **Instagram Embeds**: View Instagram posts directly in the dashboard
- **Random Inspiration**: Discover forgotten saves with a random button

## 🏗️ Architecture

```
┌─────────────┐
│  WhatsApp   │
│     User    │
└──────┬──────┘
       │ Sends Link
       ▼
┌─────────────────┐
│  Twilio Webhook │
│   (Flask App)   │
└──────┬──────────┘
       │
       ├──► Extract Content (Instagram/Twitter/Article)
       │
       ├──► OpenAI API (Tag & Summarize)
       │
       └──► SQLite Database
              │
              ▼
       ┌──────────────┐
       │   Dashboard  │
       │  (Web Page)  │
       └──────────────┘
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
OPENAI_API_KEY=sk-your-openai-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
```

### 3. Get API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add it to `.env`

#### Twilio Setup
1. Sign up at https://www.twilio.com/try-twilio
2. Get your Account SID and Auth Token from the dashboard
3. Set up WhatsApp Sandbox:
   - Go to Messaging > Try it out > Send a WhatsApp message
   - Follow instructions to join the sandbox
   - Note your sandbox number
4. Configure webhook URL in Twilio Console:
   - Go to Phone Numbers > Manage > Active numbers
   - Click on your WhatsApp sandbox number
   - Set webhook URL to: `https://your-domain.com/webhook`
   - For local testing, use ngrok: `ngrok http 5000`

### 4. Run the Application

```bash
python app.py
```

The app will run on `http://localhost:5000`

### 5. Expose with ngrok (for local testing)

```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) and use it as your webhook URL in Twilio.

## 📱 Usage

1. **Send a link via WhatsApp** to your Twilio WhatsApp number:
   ```
   https://instagram.com/p/xyz123
   ```

2. **Bot responds** with confirmation:
   ```
   ✅ Got it! Saved to your 'Fitness' bucket.
   
   📝 Great workout routine for abs...
   ```

3. **View on dashboard**: Visit `http://localhost:5000` to see all your saves

4. **Search**: Use the search bar to find specific content (e.g., "Pasta", "Coding")

5. **Random Inspiration**: Click "Random Inspiration" to discover forgotten saves

## 🗂️ Database Schema

The SQLite database (`saves.db`) stores:

- `id`: Unique identifier
- `url`: Original link
- `platform`: instagram, twitter, or article
- `caption`: Extracted caption/text
- `hashtags`: Comma-separated hashtags
- `category`: AI-generated category
- `summary`: AI-generated summary
- `created_at`: Timestamp

## 🎨 Dashboard Features

- **Card Layout**: Beautiful card-based display
- **Platform Badges**: Color-coded badges for Instagram, Twitter, Articles
- **Category Tags**: Visual category indicators
- **Search**: Real-time search across captions, categories, and hashtags
- **Instagram Embeds**: Embedded Instagram posts (when available)
- **Responsive Design**: Works on mobile and desktop

## 🔧 API Endpoints

- `GET /` - Dashboard homepage
- `GET /api/saves?search=query` - Get all saves (optionally filtered)
- `GET /api/random` - Get a random save
- `POST /webhook` - Twilio webhook for WhatsApp messages

## 🛠️ Technologies Used

- **Flask**: Python web framework
- **Twilio**: WhatsApp API integration
- **OpenAI GPT-3.5**: AI categorization and summarization
- **SQLite**: Lightweight database
- **BeautifulSoup**: Web scraping for content extraction
- **HTML/CSS/JavaScript**: Dashboard frontend

## 📝 Notes

- Instagram content extraction may be limited due to Instagram's restrictions. For production, consider using Instagram Basic Display API.
- The bot works best with public Instagram posts and Twitter links.
- OpenAI API usage will incur costs based on your usage.

## 🎯 Evaluation Criteria Coverage

✅ **WhatsApp → Insta Flow (40%)**: Complete flow from WhatsApp to dashboard  
✅ **AI Smarts (30%)**: Auto-tagging and summarization with OpenAI  
✅ **User Experience (20%)**: Clean dashboard with search functionality  
✅ **Wow Factor (10%)**: Instagram embeds and random inspiration feature  

## 📄 License

MIT License - Feel free to use this for your hackathon!
