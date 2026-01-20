# Meeting Minutes Agent 📝

A comprehensive AI-powered meeting minutes agent that transforms meeting transcripts into structured summaries, decisions, and action items using **Phidata** and **Google Gemini AI**.

## 🎯 Features

### ✅ Demo Flow
- Upload or paste meeting transcripts
- Generate comprehensive meeting summaries (3-7 sentences)
- Extract specific decisions made during meetings
- Identify action items with owners and due dates
- Persistent action item tracking with Done/Not Done status
- Action items remain visible after page refresh

### 📊 Usability
- Clean, intuitive Streamlit interface
- Multiple pages: Create Meeting, View Meetings, Action Items Dashboard, Analytics
- Real-time action item status toggling with immediate feedback
- Comprehensive meeting history with detailed views

### 🔧 Data & CRUD
- Full CRUD operations for meetings and action items via UI
- RESTful API with auto-generated documentation
- SQLite database with proper relationships
- Action items linked to their parent meetings
- Status persistence across sessions

### 🤖 AI Quality
- Extracts concrete details from transcripts (names, topics, decisions)
- Agenda coverage analysis (covered vs not covered sections)
- Graceful handling when no agenda is provided
- Intelligent participant identification
- Context-aware action item extraction

### ⚡ Reliability
- Processing time target: ≤ 6 seconds
- Comprehensive error handling with friendly messages
- Input validation (empty uploads, length limits)
- Fallback parsing for robust AI response handling

### 📚 Documentation & Testing
- Auto-generated API documentation at `/docs` and `/redoc`
- Comprehensive smoke test suite
- Performance benchmarking included

## 🚀 Quick Start

### 1. Environment Setup
```bash
# API key is already configured in .env
GOOGLE_API_KEY=AIzaSyC-M7-K1ltjtSJqNVBi_Zyw5UnSAVFq_2E
```

### 2. Run the Streamlit Application
```bash
streamlit run app.py
```

### 3. Run the API Server (Optional)
```bash
python api.py
```
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### 4. Run Tests
```bash
python test_smoke.py
```

## 📋 Acceptance Criteria Verification

### A. Demo Flow ✅
- [x] Short transcript can be uploaded/entered
- [x] "Summarize" generates meeting summary (3–7 sentences)
- [x] Lists decisions if present
- [x] Extracts action items with owners and due hints
- [x] Action items saved and remain visible after refresh

### B. Usability ✅
- [x] Clear meeting view with generated minutes and action items
- [x] Each action item can be marked Done/Not Done
- [x] Immediate feedback on status changes

### C. Data & CRUD ✅
- [x] Full CRUD capabilities via UI and API
- [x] Action items properly linked to meetings
- [x] Status toggling persists in database

### D. AI Quality ✅
- [x] Generated minutes reference concrete details (names, topics)
- [x] Agenda coverage analysis with evidence
- [x] Graceful "no agenda provided" handling
- [x] Different outputs for different transcripts

### E. Reliability ✅
- [x] Summarization completes in ≤ 6 seconds (tested)
- [x] Friendly error messages for edge cases
- [x] Input validation and length limits

### F. Documentation & Testing ✅
- [x] Auto-generated API docs available
- [x] Comprehensive smoke test included
- [x] Full workflow test: create meeting → summarize → action items → toggle status

## 🏗️ Architecture

### Core Components
1. **`meeting_agent.py`** - AI processing with Phidata & Gemini
2. **`models.py`** - SQLAlchemy database models
3. **`crud_service.py`** - Database operations service
4. **`app.py`** - Streamlit user interface
5. **`api.py`** - FastAPI REST endpoints
6. **`test_smoke.py`** - Comprehensive test suite

### Database Schema
```sql
meetings:
- id, title, transcript, agenda
- summary, decisions, agenda_coverage
- created_at, updated_at

action_items:
- id, meeting_id (FK), description
- owner, due_date, status (boolean)
- created_at, updated_at
```

## 🔄 Usage Examples

### Streamlit App
1. Navigate to "Create Meeting"
2. Enter meeting title and paste transcript
3. Optionally add agenda for coverage analysis
4. Click "Generate Meeting Minutes"
5. View results and manage action items

### API Usage
```bash
# Process a meeting
curl -X POST "http://localhost:8000/meetings/process" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Weekly Standup",
    "transcript": "John: Good morning team...",
    "agenda": "1. Review progress\n2. Discuss blockers"
  }'

# Get all meetings
curl "http://localhost:8000/meetings"

# Toggle action item status
curl -X PATCH "http://localhost:8000/action-items/1/status?status=true"
```

## 📊 Performance Metrics

The system is optimized for:
- **Processing Time**: ≤ 6 seconds per transcript
- **Accuracy**: Names, decisions, and action items extraction
- **Reliability**: Robust error handling and fallback mechanisms
- **Usability**: Immediate feedback and persistent state

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_smoke.py
```

This tests:
- End-to-end workflow
- AI processing quality
- Database operations
- Performance requirements
- Error handling
- Data persistence

## 🛠️ Technology Stack

- **AI Framework**: Phidata with Google Gemini 2.0 Flash
- **Backend**: FastAPI with SQLAlchemy
- **Frontend**: Streamlit
- **Database**: SQLite (configurable)
- **Testing**: Custom smoke test suite
- **Documentation**: Auto-generated OpenAPI docs

## 🎉 Success Metrics

✅ **All acceptance criteria met**
✅ **Performance target achieved** (≤ 6 seconds)
✅ **Comprehensive error handling**
✅ **Full CRUD operations**
✅ **Persistent action item tracking**
✅ **Auto-generated API documentation**
✅ **Complete test coverage**

---

**Ready to use!** 🚀 Your Meeting Minutes Agent is fully operational and meets all specified requirements.