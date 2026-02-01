# 📝 End-to-End Agentic AI Meeting Intelligence

An intelligent AI-powered meeting management system that automatically transcribes meetings, generates summaries, extracts key decisions, identifies action items, and tracks meeting outcomes using **Google Gemini AI** and **Phidata**.

This project demonstrates a real-world AI pipeline combining multimedia processing, speech transcription, and agent-based reasoning to transform unstructured meeting data into actionable intelligence.

---

## 🌟 Features

### Core Capabilities
- 🎤 **Audio/Video Transcription**: Upload audio or video files and automatically convert speech to text
- 🤖 **AI-Powered Analysis**: Uses Google Gemini AI with Phidata to extract structured information
- 📊 **Smart Summarization**: Generates concise meeting summaries highlighting key topics and outcomes
- ✅ **Action Item Extraction**: Automatically identifies tasks, assignees, and due dates
- 📋 **Decision Tracking**: Captures specific decisions made during meetings
- 📝 **Agenda Coverage Analysis**: Tracks which agenda items were discussed and which were missed
- 👥 **Participant Identification**: Extracts names of meeting participants from transcripts

### Interfaces
- 🌐 **Streamlit Web UI**: User-friendly interface for creating and viewing meetings
- 🔌 **REST API**: Full-featured FastAPI backend for programmatic access
- 💾 **Database Storage**: SQLite/PostgreSQL support for persistent data storage

### Supported Media Formats
- **Audio**: MP3, WAV, M4A
- **Video**: MP4, MOV, AVI, WebM (audio automatically extracted via FFmpeg)
- **Text**: Direct transcript paste

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│  ┌────────────────┐              ┌──────────────────┐       │
│  │  Streamlit UI  │              │   FastAPI REST   │       │
│  │   (app.py)     │              │   API (api.py)   │       │
│  └────────────────┘              └──────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  MeetingMinutesAgent (meeting_agent.py)              │   │
│  │  • AI Analysis with Google Gemini                    │   │
│  │  • Structured Information Extraction                 │   │
│  │  • Phidata Agent Framework                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CRUDService (crud_service.py)                       │   │
│  │  • Database Operations                               │   │
│  │  • Meeting & Action Item Management                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Video/Audio Utils (video_utils.py)                  │   │
│  │  • FFmpeg Integration                                │   │
│  │  • Audio Extraction from Video                       │   │
│  │  • Speech Recognition                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SQLAlchemy Models (models.py)                       │   │
│  │  • Meeting Model                                     │   │
│  │  • ActionItem Model                                  │   │
│  │  • Database Schema                                   │   │
│  └──────────────────────────────────────────────────────┘   │ 
│                                                             │
│           SQLite / PostgreSQL Database                      │
└─────────────────────────────────────────────────────────────┘
```

### Agentic Workflow
The system follows a multi-agent workflow:

1. **Input Agent**: Handles transcript, audio, or video input
2. **Media Processing Agent**: Extracts audio from video using FFmpeg
3. **Transcription Agent**: Converts audio into text using speech recognition
4. **Reasoning Agent (LLM)**: Analyzes transcript to generate structured meeting intelligence
5. **Persistence Agent**: Stores meetings, action items, and analytics
6. **UI Agent**: Presents insights via Streamlit or REST API

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** 
- **FFmpeg** (for video/audio processing)
- **Google Gemini API key**

### Installation Steps

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/mrcoolash/End-to-End-Agentic-AI-Meeting-Intelligence.git
cd End-to-End-Agentic-AI-Meeting-Intelligence
```

#### 2️⃣ Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ Install FFmpeg

**Windows:**
1. Download from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
2. Extract and add to system PATH
3. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

#### 5️⃣ Configure Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=sqlite:///meetings.db
```

**To get a Google Gemini API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

#### 6️⃣ Run the Application

**Option A: Streamlit Web Interface** (Recommended for Users)
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`

**Option B: FastAPI REST API** (Recommended for Developers)
```bash
python api.py
```
API documentation available at:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 📖 Usage Guide

### Using the Streamlit Interface

#### Creating a Meeting
1. Navigate to **Create Meeting** page
2. Enter a **Meeting Title**
3. Choose input method:
   - **Paste Transcript**: Directly paste meeting transcript text
   - **Upload Audio/Video**: Upload MP3, WAV, MP4, MOV, AVI, or WebM files
4. If uploading media, click **🎤 Transcribe**
5. (Optional) Add **Agenda Items**
6. Click **🚀 Generate Meeting Minutes**

The AI will:
- Generate a comprehensive summary
- Extract key decisions
- Identify action items with owners and due dates
- Analyze agenda coverage
- Identify participants

#### Viewing Past Meetings
1. Navigate to **View Meetings** page
2. Browse all processed meetings
3. Expand any meeting to see full details including:
   - Summary
   - Decisions
   - Action items
   - Transcript

### Using the REST API

#### Process a Meeting
```bash
POST http://127.0.0.1:8000/meetings/process
Content-Type: application/json

{
  "title": "Q1 Planning Meeting",
  "transcript": "John: Let's discuss our Q1 goals. Sarah: I think we should focus on customer retention...",
  "agenda": "1. Review Q1 objectives\n2. Budget allocation\n3. Team assignments"
}
```

#### Get All Meetings
```bash
GET http://127.0.0.1:8000/meetings
```

#### Get Specific Meeting with Action Items
```bash
GET http://127.0.0.1:8000/meetings/{meeting_id}
```

#### Get All Action Items
```bash
GET http://127.0.0.1:8000/action-items
GET http://127.0.0.1:8000/meetings/{meeting_id}/action-items
```

#### Update Action Item Status
```bash
PATCH http://127.0.0.1:8000/action-items/{item_id}/status?status=true
```

#### Get Analytics Summary
```bash
GET http://127.0.0.1:8000/analytics/summary
```

---

## 📁 Project Structure

```
End-to-End-Agentic-AI-Meeting-Intelligence/
│
├── app.py                  # Streamlit web interface
├── api.py                  # FastAPI REST API server
├── meeting_agent.py        # AI agent for meeting analysis (Gemini + Phidata)
├── crud_service.py         # Database CRUD operations
├── models.py              # SQLAlchemy database models
├── video_utils.py         # Audio/video processing utilities (FFmpeg)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
├── LICENSE               # License file
├── README.md             # This file
└── meetings.db           # SQLite database (auto-generated)
```

---

## 🛠️ Technology Stack

### AI & ML
- **Google Gemini AI** (gemini-2.0-flash-exp): Advanced language model for text analysis
- **Phidata**: Agent framework for structured AI workflows
- **SpeechRecognition**: Audio-to-text transcription
- **DuckDuckGo Search**: Web search integration for context

### Backend
- **FastAPI**: High-performance REST API framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server

### Frontend
- **Streamlit**: Interactive web interface

### Media Processing
- **FFmpeg**: Video/audio extraction and processing
- **Pydub**: Audio file manipulation

### Database
- **SQLite**: Default lightweight database
- **PostgreSQL**: Production-ready option (configurable via `DATABASE_URL`)

---

## 📊 Database Schema

### Meeting Table
```sql
CREATE TABLE meetings (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    transcript TEXT NOT NULL,
    agenda TEXT,
    summary TEXT,
    decisions TEXT,              -- JSON array
    agenda_coverage TEXT,        -- JSON object
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ActionItem Table
```sql
CREATE TABLE action_items (
    id INTEGER PRIMARY KEY,
    meeting_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    owner VARCHAR(255),
    due_date VARCHAR(100),
    status BOOLEAN DEFAULT FALSE, -- True=Done, False=Pending
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
);
```

---

## 🔑 Key Features Explained

### AI Meeting Analysis
The system uses **Google Gemini AI** to perform sophisticated natural language processing:
- Extracts meaningful summaries from raw transcripts
- Identifies explicit decisions vs. general discussions
- Detects action items with ownership and deadlines
- Analyzes agenda coverage with evidence from transcripts
- Identifies meeting participants automatically

### Structured Output Format
All AI analysis results in structured JSON format:
```json
{
  "summary": "3-7 sentence summary highlighting key topics and outcomes",
  "decisions": [
    "Specific decision 1",
    "Specific decision 2"
  ],
  "action_items": [
    {
      "description": "Task description",
      "owner": "Person name",
      "due_date": "Timeframe or date"
    }
  ],
  "agenda_coverage": {
    "status": "covered",
    "covered_items": [
      {
        "item": "Agenda item text",
        "evidence": "Quote from transcript"
      }
    ],
    "uncovered_items": ["Missed agenda items"]
  },
  "participants": ["John", "Sarah", "Mike"],
  "key_topics": ["Topic 1", "Topic 2"]
}
```

---

## 🔒 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | - | Google Gemini API key from AI Studio |
| `DATABASE_URL` | ❌ No | `sqlite:///meetings.db` | Database connection string |

---

## 🐛 Troubleshooting

### Issue: "FFmpeg not found"
**Solution**: Install FFmpeg and add it to your system PATH
```bash
# Verify installation
ffmpeg -version
```

### Issue: "Set GOOGLE_API_KEY in .env"
**Solution**: Create `.env` file with your API key
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

### Issue: "Module not found" errors
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Database errors
**Solution**: Delete `meetings.db` file and restart (tables will be recreated automatically)
```bash
rm meetings.db  # or delete manually
python app.py   # or streamlit run app.py
```

### Issue: Transcription fails
**Solution**: 
- Ensure audio quality is good (clear speech, minimal background noise)
- Check internet connection (Google Speech Recognition requires internet)
- Try converting audio to WAV format first

---

## 📝 API Endpoints Reference

### Health
- `GET /` - Basic health check
- `GET /health` - Detailed health status

### Meetings
- `POST /meetings/process` - Process meeting transcript with AI
- `GET /meetings` - List all meetings (with pagination)
- `GET /meetings/{id}` - Get specific meeting with details
- `DELETE /meetings/{id}` - Delete meeting and related action items

### Action Items
- `GET /action-items` - List all action items across all meetings
- `GET /meetings/{id}/action-items` - Get action items for specific meeting
- `POST /action-items` - Create new action item
- `PUT /action-items/{id}` - Update action item
- `PATCH /action-items/{id}/status` - Toggle completion status
- `DELETE /action-items/{id}` - Delete action item

### Analytics
- `GET /analytics/summary` - Get analytics summary (totals, completion rates)

---

## ⚙️ Configuration Notes

### Files Not Committed to Git
- `.env` - Environment variables (contains API keys)
- `venv/` - Virtual environment
- `__pycache__/` - Python cache files
- `meetings.db` - SQLite database
- `session_state.json` - Streamlit session state

### System Requirements
- **FFmpeg** must be available in system PATH
- **Internet connection** required for:
  - Google Gemini API calls
  - Speech recognition (Google Speech API)
  - DuckDuckGo search tool

---

## 📌 Future Enhancements

- 🔗 **YouTube/URL Integration**: Direct video summarization from URLs
- 🧠 **RAG-based Memory**: Long-term meeting memory with vector search
- 👥 **Speaker Diarization**: Identify who said what
- 🌍 **Multilingual Support**: Transcription in multiple languages
- ☁️ **Cloud Deployment**: Deploy on Streamlit Cloud or Hugging Face
- 📅 **Calendar Integration**: Sync with Google Calendar, Outlook
- 📧 **Email Notifications**: Automatic action item reminders
- 🎯 **Custom Prompts**: User-defined extraction templates
- 📱 **Mobile App**: React Native or Flutter mobile interface
- 🔐 **Authentication**: User accounts and permissions

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas of interest:
- Additional LLM support (OpenAI GPT-4, Anthropic Claude)
- Real-time transcription during live meetings
- Integration with collaboration tools (Slack, Teams, Zoom)
- Enhanced analytics and visualizations
- Performance optimizations

---

## 📄 License

See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Vishnu Ashrith**  
Electronics & Communication Engineering  
AI / Machine Learning Enthusiast

---

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language model capabilities
- **Phidata** for agent orchestration framework
- **Streamlit** for rapid UI development
- **FastAPI** for high-performance API framework
- **FFmpeg** community for multimedia processing tools

---

**Built with ❤️ for better meeting management and productivity**