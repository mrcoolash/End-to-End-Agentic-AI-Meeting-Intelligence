# 🎯 End-To-End Meeting Minutes Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent AI-powered meeting minutes generator that transforms audio recordings and transcripts into comprehensive, actionable meeting summaries with automated action item tracking.

## 🌟 Features

### 🎤 Multi-Modal Input Support
- **Audio File Upload**: Support for MP3, WAV, M4A, MP4, WebM formats
- **Live Audio Recording**: Browser-based audio recording capability
- **Direct Transcript Input**: Paste meeting transcripts directly
- **FFmpeg Integration**: Automatic audio format conversion

### 🤖 AI-Powered Processing
- **Google Gemini Integration**: Advanced natural language processing
- **Intelligent Summarization**: Contextual meeting summaries
- **Decision Extraction**: Automatically identifies key decisions
- **Action Item Detection**: Smart action item generation with assignees and due dates

### 📊 Comprehensive Management
- **Meeting History**: Complete record of all processed meetings
- **Action Items Dashboard**: Interactive tracking with completion status
- **Analytics**: Meeting insights and productivity metrics
- **Agenda Coverage Analysis**: Tracks discussed vs. planned topics

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python 3.8 or higher
python --version

# Install FFmpeg (required for audio processing)
# Windows (using winget):
winget install "FFmpeg (Essentials Build)"

# macOS (using Homebrew):
brew install ffmpeg

# Linux (Ubuntu/Debian):
sudo apt update && sudo apt install ffmpeg
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AnshKumar6400/End-To-End-Video-Summarizer-Agentic-AI.git
cd End-To-End-Video-Summarizer-Agentic-AI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create a .env file in the project root
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
```

> 🔑 **Get your Google API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to obtain your Gemini API key.

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the app**
Open your browser and navigate to `http://localhost:8501`

## 🎮 Usage Guide

### 1. Create a New Meeting
1. Enter a descriptive meeting title
2. Choose your input method:
   - **Upload Audio**: Select and upload audio files
   - **Record Audio**: Use browser recording (preview feature)
   - **Paste Transcript**: Direct text input

### 2. Audio Processing
- Upload supported audio formats (WAV recommended)
- Click "🎤 Transcribe Audio" to convert speech to text
- Review and edit the generated transcript

### 3. Generate Minutes
- Add optional meeting agenda for coverage analysis
- Click "🔄 Generate Meeting Minutes"
- AI processes the content and generates:
  - Executive summary
  - Key decisions made
  - Action items with assignments
  - Agenda coverage report

### 4. Manage Action Items
- Track completion status
- Update assignees and due dates
- Mark items as completed
- Export for external project management tools

## 🛠️ Technology Stack

- **Frontend**: Streamlit for interactive web interface
- **AI Model**: Google Gemini AI for natural language processing
- **Audio Processing**: SpeechRecognition + pydub + FFmpeg
- **Database**: SQLAlchemy with SQLite for data persistence
- **Session Management**: Streamlit session state with local storage

## 📈 Performance

- **Processing Speed**: ≤6 seconds target for transcript analysis
- **Audio Support**: Up to 20,000 characters transcript length
- **Storage**: Efficient SQLite storage with session persistence
- **Scalability**: Single-user optimized, multi-user capable

## 🐛 Troubleshooting

### Common Issues

**Audio transcription fails**
- Ensure FFmpeg is installed and in PATH
- Try WAV format if other formats fail
- Check audio quality and clarity

**API errors**
- Verify Google API key is correct
- Check API quota and billing
- Ensure internet connectivity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language processing
- **Streamlit** for the excellent web framework
- **Speech Recognition** library for audio processing
- **SQLAlchemy** for robust data management

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [AnshKumar6400](https://github.com/AnshKumar6400)

</div>

