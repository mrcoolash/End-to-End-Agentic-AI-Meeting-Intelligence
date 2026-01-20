import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict
import os
import tempfile
from dotenv import load_dotenv

# NEW: video utility
from video_utils import extract_audio_from_video

# Import custom modules
from meeting_agent import MeetingMinutesAgent
from crud_service import CRUDService

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Meeting Minutes Agent",
    page_icon="📝",
    layout="wide"
)

# Initialize services
@st.cache_resource
def initialize_services():
    return {
        "meeting_agent": MeetingMinutesAgent(),
        "crud_service": CRUDService()
    }

services = initialize_services()

# ---------------- SESSION STATE ---------------- #

def save_session_state():
    try:
        with open("session_state.json", "w") as f:
            json.dump({
                "current_page": st.session_state.get("current_page", "Create Meeting"),
                "transcribed_audio_text": st.session_state.get("transcribed_audio_text", "")
            }, f)
    except:
        pass

def load_session_state():
    if os.path.exists("session_state.json"):
        with open("session_state.json", "r") as f:
            data = json.load(f)
            for k, v in data.items():
                if k not in st.session_state:
                    st.session_state[k] = v

load_session_state()

# ---------------- AUDIO TRANSCRIPTION ---------------- #

def transcribe_audio(audio_path: str) -> str:
    import speech_recognition as sr
    from pydub import AudioSegment

    recognizer = sr.Recognizer()
    wav_path = audio_path

    if not audio_path.endswith(".wav"):
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.replace(os.path.splitext(audio_path)[1], ".wav")
        audio.export(wav_path, format="wav")

    with sr.AudioFile(wav_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)

    text = recognizer.recognize_google(audio_data)

    if wav_path != audio_path and os.path.exists(wav_path):
        os.remove(wav_path)

    return text

# ---------------- UI ---------------- #

st.title("Meeting Minutes Agent 📝")
st.markdown("**End-to-End Agentic AI Meeting Intelligence**")

if not os.getenv("GOOGLE_API_KEY"):
    st.error("Set GOOGLE_API_KEY in .env")
    st.stop()

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose Page",
    ["Create Meeting", "View Meetings"],
    index=0
)

# ---------------- CREATE MEETING ---------------- #

if page == "Create Meeting":
    st.header("📝 Create New Meeting")

    meeting_title = st.text_input("Meeting Title")

    input_method = st.selectbox(
        "Input Method",
        ["Paste Transcript", "Upload Audio / Video"]
    )

    transcript = ""

    # ---------- PASTE TRANSCRIPT ---------- #
    if input_method == "Paste Transcript":
        transcript = st.text_area(
            "Meeting Transcript",
            value=st.session_state.get("transcribed_audio_text", ""),
            height=200
        )

    # ---------- UPLOAD AUDIO / VIDEO ---------- #
    elif input_method == "Upload Audio / Video":
        audio_file = st.file_uploader(
            "Upload Audio or Video File",
            type=["wav", "mp3", "m4a", "mp4", "mov", "avi", "webm"]
        )

        if audio_file:
            ext = audio_file.name.split(".")[-1].lower()

            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
                tmp.write(audio_file.getvalue())
                uploaded_path = tmp.name

            # VIDEO → AUDIO
            if ext in ["mp4", "mov", "avi", "webm"]:
                st.info("🎥 Video detected — extracting audio using FFmpeg...")
                audio_path = extract_audio_from_video(uploaded_path)
            else:
                audio_path = uploaded_path

            if st.button("🎤 Transcribe"):
                with st.spinner("Transcribing..."):
                    try:
                        transcript = transcribe_audio(audio_path)
                        st.session_state.transcribed_audio_text = transcript
                        save_session_state()
                        st.success("Transcription successful!")
                        st.text_area("Transcript Preview", transcript, height=150)
                    except Exception as e:
                        st.error(f"Transcription failed: {e}")

            # cleanup
            if os.path.exists(uploaded_path):
                os.remove(uploaded_path)
            if audio_path != uploaded_path and os.path.exists(audio_path):
                os.remove(audio_path)

    agenda = st.text_area("Agenda (Optional)", height=100)

    if st.button("🚀 Generate Meeting Minutes", type="primary"):
        if not meeting_title or not transcript.strip():
            st.error("Meeting title and transcript are required")
        else:
            with st.spinner("AI is analyzing the meeting..."):
                result = services["meeting_agent"].process_meeting_transcript(
                    transcript=transcript,
                    agenda=agenda if agenda else None,
                    meeting_title=meeting_title
                )

                if result.get("success"):
                    meeting = services["crud_service"].create_meeting(
                        title=meeting_title,
                        transcript=transcript,
                        agenda=agenda,
                        summary=result["summary"],
                        decisions=result["decisions"],
                        agenda_coverage=result["agenda_coverage"]
                    )

                    st.success("Meeting processed successfully!")
                    st.subheader("📝 Summary")
                    st.write(result["summary"])

                    if result["decisions"]:
                        st.subheader("📋 Decisions")
                        for d in result["decisions"]:
                            st.write(f"- {d}")

                    if result["action_items"]:
                        st.subheader("✅ Action Items")
                        for a in result["action_items"]:
                            st.write(f"- {a['description']}")
                else:
                    st.error("AI processing failed")

# ---------------- VIEW MEETINGS ---------------- #

elif page == "View Meetings":
    st.header("📁 Past Meetings")

    meetings = services["crud_service"].get_all_meetings()
    if not meetings:
        st.info("No meetings yet.")
    else:
        for m in meetings:
            with st.expander(m.title):
                st.write(m.summary)
