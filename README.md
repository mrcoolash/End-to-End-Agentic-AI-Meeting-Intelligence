End-to-End Agentic AI Meeting Intelligence

An end-to-end Agentic AI system that transforms meeting audio and video into structured intelligence — including summaries, decisions, and action items — using LLMs, FFmpeg, and Streamlit.

This project demonstrates a real-world AI pipeline combining multimedia processing, speech transcription, and agent-based reasoning.

Features

🎥 Audio & Video Input Support (MP3, WAV, MP4, MOV, AVI, WebM)

🔊 Automatic Video → Audio Extraction using FFmpeg

📝 Speech-to-Text Transcription

🧠 Agentic AI Reasoning to extract:

Meeting summary

Decisions made

Action items with owners

 Meeting history & analytics

⚡ Interactive Streamlit UI

🧩 Agentic Architecture (High-Level)

The system follows a multi-agent workflow:

Input Agent
Handles transcript, audio, or video input.

Media Processing Agent
Extracts audio from video using FFmpeg.

Transcription Agent
Converts audio into text using speech recognition.

Reasoning Agent (LLM)
Analyzes transcript to generate structured meeting intelligence.

Persistence Agent
Stores meetings, action items, and analytics.

UI Agent
Presents insights via Streamlit.

🛠 Tech Stack

Python

Streamlit

FFmpeg

SpeechRecognition

Google Gemini / LLM APIs

SQLite

Agent-based AI design

▶️ How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/mrcoolash/End-to-End-Agentic-AI-Meeting-Intelligence.git
cd End-to-End-Agentic-AI-Meeting-Intelligence

2️⃣ Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variables

Create a .env file in the project root:

GOOGLE_API_KEY=your_google_api_key_here

5️⃣ Ensure FFmpeg is installed

Verify FFmpeg:

ffmpeg -version


If not installed, download from:
https://www.gyan.dev/ffmpeg/builds/

6️⃣ Run the application
streamlit run app.py

⚙️ Configuration Notes

.env, venv/, __pycache__/, meetings.db, and session_state.json are not committed

FFmpeg must be available in system PATH

GitHub authentication uses Personal Access Tokens

📌 Future Enhancements

🔗 YouTube / URL-based video summarization

🧠 RAG-based long-term meeting memory

👥 Speaker diarization

🌍 Multilingual transcription

☁️ Cloud deployment (Streamlit Cloud / Hugging Face)

📅 Calendar & task integrations

Author

Vishnu Ashrith
Electronics & Communication Engineering
AI / Machine Learning Enthusiast