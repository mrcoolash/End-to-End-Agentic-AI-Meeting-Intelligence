"""
FastAPI endpoints for Meeting Minutes Agent
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime

from meeting_agent import MeetingMinutesAgent
from crud_service import CRUDService
from models import Meeting, ActionItem

# Initialize FastAPI app
app = FastAPI(
    title="Meeting Minutes Agent API",
    description="API for processing meeting transcripts and managing action items with AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize services
meeting_agent = MeetingMinutesAgent()
crud_service = CRUDService()

# Pydantic models for API
class MeetingCreate(BaseModel):
    title: str
    transcript: str
    agenda: Optional[str] = None

class MeetingResponse(BaseModel):
    id: int
    title: str
    transcript: str
    agenda: Optional[str]
    summary: Optional[str]
    decisions: Optional[List[str]]
    agenda_coverage: Optional[Dict]
    created_at: Optional[str]
    updated_at: Optional[str]

class ActionItemCreate(BaseModel):
    meeting_id: int
    description: str
    owner: Optional[str] = None
    due_date: Optional[str] = None

class ActionItemUpdate(BaseModel):
    description: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[bool] = None

class ActionItemResponse(BaseModel):
    id: int
    meeting_id: int
    description: str
    owner: Optional[str]
    due_date: Optional[str]
    status: bool
    created_at: Optional[str]
    updated_at: Optional[str]

class ProcessMeetingRequest(BaseModel):
    title: str
    transcript: str
    agenda: Optional[str] = None

class ProcessMeetingResponse(BaseModel):
    success: bool
    meeting_id: Optional[int]
    summary: Optional[str]
    decisions: Optional[List[str]]
    action_items: Optional[List[Dict]]
    agenda_coverage: Optional[Dict]
    processing_time: Optional[float]
    error: Optional[str]

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Meeting Minutes Agent API", 
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "meeting_agent": "available",
            "database": "connected",
            "crud_service": "available"
        },
        "timestamp": datetime.now().isoformat()
    }

# Meeting endpoints
@app.post("/meetings/process", response_model=ProcessMeetingResponse, tags=["Meetings"])
async def process_meeting(request: ProcessMeetingRequest):
    """
    Process a meeting transcript with AI to extract summary, decisions, and action items
    
    This endpoint:
    - Analyzes the transcript using AI
    - Extracts structured information (summary, decisions, action items)
    - Saves the meeting to the database
    - Creates associated action items
    - Returns processing results
    """
    try:
        # Validate input
        if not request.transcript.strip():
            raise HTTPException(status_code=400, detail="Transcript cannot be empty")
        
        if len(request.transcript) > 20000:
            raise HTTPException(status_code=400, detail="Transcript too long (max 20,000 characters)")
        
        # Process with AI
        result = meeting_agent.process_meeting_transcript(
            transcript=request.transcript,
            agenda=request.agenda,
            meeting_title=request.title
        )
        
        if not result.get('success', False):
            return ProcessMeetingResponse(
                success=False,
                error=result.get('error', 'Processing failed'),
                processing_time=result.get('processing_time')
            )
        
        # Save to database
        meeting = crud_service.create_meeting(
            title=request.title,
            transcript=request.transcript,
            agenda=request.agenda,
            summary=result.get('summary', ''),
            decisions=result.get('decisions', []),
            agenda_coverage=result.get('agenda_coverage', {})
        )
        
        # Create action items
        action_items_created = []
        if result.get('action_items'):
            action_items_created = crud_service.create_multiple_action_items(
                meeting_id=meeting.id,
                action_items_data=result['action_items']
            )
        
        return ProcessMeetingResponse(
            success=True,
            meeting_id=meeting.id,
            summary=result.get('summary'),
            decisions=result.get('decisions'),
            action_items=result.get('action_items'),
            agenda_coverage=result.get('agenda_coverage'),
            processing_time=result.get('processing_time')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/meetings", response_model=List[MeetingResponse], tags=["Meetings"])
async def get_meetings(limit: int = 50):
    """Get all meetings with optional limit"""
    try:
        meetings = crud_service.get_all_meetings(limit=limit)
        return [
            MeetingResponse(
                id=meeting.id,
                title=meeting.title,
                transcript=meeting.transcript,
                agenda=meeting.agenda,
                summary=meeting.summary,
                decisions=meeting.decisions,
                agenda_coverage=meeting.agenda_coverage,
                created_at=meeting.created_at.isoformat() if meeting.created_at else None,
                updated_at=meeting.updated_at.isoformat() if meeting.updated_at else None
            )
            for meeting in meetings
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving meetings: {str(e)}")

@app.get("/meetings/{meeting_id}", response_model=Dict, tags=["Meetings"])
async def get_meeting(meeting_id: int):
    """Get a specific meeting with its action items"""
    try:
        meeting_data = crud_service.get_meeting_with_action_items(meeting_id)
        if not meeting_data:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return meeting_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving meeting: {str(e)}")

@app.delete("/meetings/{meeting_id}", tags=["Meetings"])
async def delete_meeting(meeting_id: int):
    """Delete a meeting and all its action items"""
    try:
        success = crud_service.delete_meeting(meeting_id)
        if not success:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return {"message": "Meeting deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting meeting: {str(e)}")

# Action Item endpoints
@app.get("/action-items", response_model=List[ActionItemResponse], tags=["Action Items"])
async def get_all_action_items():
    """Get all action items across all meetings"""
    try:
        meetings = crud_service.get_all_meetings()
        all_action_items = []
        
        for meeting in meetings:
            action_items = crud_service.get_meeting_action_items(meeting.id)
            all_action_items.extend(action_items)
        
        return [
            ActionItemResponse(
                id=item.id,
                meeting_id=item.meeting_id,
                description=item.description,
                owner=item.owner,
                due_date=item.due_date,
                status=item.status,
                created_at=item.created_at.isoformat() if item.created_at else None,
                updated_at=item.updated_at.isoformat() if item.updated_at else None
            )
            for item in all_action_items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving action items: {str(e)}")

@app.get("/meetings/{meeting_id}/action-items", response_model=List[ActionItemResponse], tags=["Action Items"])
async def get_meeting_action_items(meeting_id: int):
    """Get all action items for a specific meeting"""
    try:
        action_items = crud_service.get_meeting_action_items(meeting_id)
        return [
            ActionItemResponse(
                id=item.id,
                meeting_id=item.meeting_id,
                description=item.description,
                owner=item.owner,
                due_date=item.due_date,
                status=item.status,
                created_at=item.created_at.isoformat() if item.created_at else None,
                updated_at=item.updated_at.isoformat() if item.updated_at else None
            )
            for item in action_items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving action items: {str(e)}")

@app.post("/action-items", response_model=ActionItemResponse, tags=["Action Items"])
async def create_action_item(request: ActionItemCreate):
    """Create a new action item"""
    try:
        # Verify meeting exists
        meeting = crud_service.get_meeting(request.meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        action_item = crud_service.create_action_item(
            meeting_id=request.meeting_id,
            description=request.description,
            owner=request.owner,
            due_date=request.due_date
        )
        
        return ActionItemResponse(
            id=action_item.id,
            meeting_id=action_item.meeting_id,
            description=action_item.description,
            owner=action_item.owner,
            due_date=action_item.due_date,
            status=action_item.status,
            created_at=action_item.created_at.isoformat() if action_item.created_at else None,
            updated_at=action_item.updated_at.isoformat() if action_item.updated_at else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating action item: {str(e)}")

@app.put("/action-items/{action_item_id}", response_model=ActionItemResponse, tags=["Action Items"])
async def update_action_item(action_item_id: int, request: ActionItemUpdate):
    """Update an action item"""
    try:
        action_item = crud_service.update_action_item(
            action_item_id=action_item_id,
            description=request.description,
            owner=request.owner,
            due_date=request.due_date,
            status=request.status
        )
        
        if not action_item:
            raise HTTPException(status_code=404, detail="Action item not found")
        
        return ActionItemResponse(
            id=action_item.id,
            meeting_id=action_item.meeting_id,
            description=action_item.description,
            owner=action_item.owner,
            due_date=action_item.due_date,
            status=action_item.status,
            created_at=action_item.created_at.isoformat() if action_item.created_at else None,
            updated_at=action_item.updated_at.isoformat() if action_item.updated_at else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating action item: {str(e)}")

@app.patch("/action-items/{action_item_id}/status", response_model=ActionItemResponse, tags=["Action Items"])
async def toggle_action_item_status(action_item_id: int, status: bool):
    """Toggle action item status (Done/Not Done)"""
    try:
        action_item = crud_service.update_action_item_status(action_item_id, status)
        
        if not action_item:
            raise HTTPException(status_code=404, detail="Action item not found")
        
        return ActionItemResponse(
            id=action_item.id,
            meeting_id=action_item.meeting_id,
            description=action_item.description,
            owner=action_item.owner,
            due_date=action_item.due_date,
            status=action_item.status,
            created_at=action_item.created_at.isoformat() if action_item.created_at else None,
            updated_at=action_item.updated_at.isoformat() if action_item.updated_at else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating action item status: {str(e)}")

@app.delete("/action-items/{action_item_id}", tags=["Action Items"])
async def delete_action_item(action_item_id: int):
    """Delete an action item"""
    try:
        success = crud_service.delete_action_item(action_item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Action item not found")
        return {"message": "Action item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting action item: {str(e)}")

# Analytics endpoints
@app.get("/analytics/summary", tags=["Analytics"])
async def get_analytics_summary():
    """Get analytics summary of meetings and action items"""
    try:
        action_items_summary = crud_service.get_action_items_summary()
        meetings = crud_service.get_all_meetings()
        
        # Calculate meeting statistics
        total_meetings = len(meetings)
        avg_action_items = action_items_summary['total_action_items'] / total_meetings if total_meetings > 0 else 0
        
        return {
            "meetings": {
                "total_meetings": total_meetings,
                "avg_action_items_per_meeting": round(avg_action_items, 1)
            },
            "action_items": action_items_summary,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating analytics: {str(e)}")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.now().isoformat()}
    )

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "api:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )