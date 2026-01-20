"""
Database models for the Meeting Minutes Agent
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    transcript = Column(Text, nullable=False)
    agenda = Column(Text, nullable=True)  # Optional agenda
    summary = Column(Text, nullable=True)  # AI-generated summary
    decisions = Column(Text, nullable=True)  # AI-extracted decisions
    agenda_coverage = Column(Text, nullable=True)  # JSON string of covered/uncovered items
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship to action items
    action_items = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")

class ActionItem(Base):
    __tablename__ = "action_items"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    description = Column(Text, nullable=False)
    owner = Column(String(255), nullable=True)  # Person responsible
    due_date = Column(String(100), nullable=True)  # Due date hint from AI
    status = Column(Boolean, default=False)  # True = Done, False = Not Done
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship back to meeting
    meeting = relationship("Meeting", back_populates="action_items")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///meetings.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()