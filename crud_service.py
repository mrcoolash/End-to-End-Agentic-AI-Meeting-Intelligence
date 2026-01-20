"""
CRUD operations for meetings and action items
"""
import json
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from models import Meeting, ActionItem, get_db, create_tables
from datetime import datetime

class CRUDService:
    def __init__(self):
        # Create tables if they don't exist
        create_tables()
    
    def get_db_session(self):
        """Get a database session"""
        return next(get_db())
    
    # Meeting CRUD operations
    def create_meeting(
        self, 
        title: str, 
        transcript: str, 
        agenda: Optional[str] = None,
        summary: Optional[str] = None,
        decisions: Optional[List[str]] = None,
        agenda_coverage: Optional[Dict] = None
    ) -> Meeting:
        """Create a new meeting record"""
        db = self.get_db_session()
        try:
            meeting = Meeting(
                title=title,
                transcript=transcript,
                agenda=agenda,
                summary=summary,
                decisions=json.dumps(decisions) if decisions else None,
                agenda_coverage=json.dumps(agenda_coverage) if agenda_coverage else None
            )
            db.add(meeting)
            db.commit()
            db.refresh(meeting)
            return meeting
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_meeting(self, meeting_id: int) -> Optional[Meeting]:
        """Get a meeting by ID"""
        db = self.get_db_session()
        try:
            return db.query(Meeting).filter(Meeting.id == meeting_id).first()
        finally:
            db.close()
    
    def get_all_meetings(self, limit: int = 50) -> List[Meeting]:
        """Get all meetings ordered by creation date (newest first)"""
        db = self.get_db_session()
        try:
            return db.query(Meeting).order_by(Meeting.created_at.desc()).limit(limit).all()
        finally:
            db.close()
    
    def update_meeting(
        self, 
        meeting_id: int, 
        title: Optional[str] = None,
        summary: Optional[str] = None,
        decisions: Optional[List[str]] = None,
        agenda_coverage: Optional[Dict] = None
    ) -> Optional[Meeting]:
        """Update a meeting record"""
        db = self.get_db_session()
        try:
            meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
            if not meeting:
                return None
            
            if title is not None:
                meeting.title = title
            if summary is not None:
                meeting.summary = summary
            if decisions is not None:
                meeting.decisions = json.dumps(decisions)
            if agenda_coverage is not None:
                meeting.agenda_coverage = json.dumps(agenda_coverage)
            
            meeting.updated_at = datetime.now()
            db.commit()
            db.refresh(meeting)
            return meeting
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def delete_meeting(self, meeting_id: int) -> bool:
        """Delete a meeting and its action items"""
        db = self.get_db_session()
        try:
            meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
            if not meeting:
                return False
            
            db.delete(meeting)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    # Action Item CRUD operations
    def create_action_item(
        self, 
        meeting_id: int, 
        description: str, 
        owner: Optional[str] = None, 
        due_date: Optional[str] = None
    ) -> ActionItem:
        """Create a new action item"""
        db = self.get_db_session()
        try:
            action_item = ActionItem(
                meeting_id=meeting_id,
                description=description,
                owner=owner,
                due_date=due_date,
                status=False
            )
            db.add(action_item)
            db.commit()
            db.refresh(action_item)
            return action_item
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def create_multiple_action_items(self, meeting_id: int, action_items_data: List[Dict]) -> List[ActionItem]:
        """Create multiple action items for a meeting"""
        db = self.get_db_session()
        try:
            action_items = []
            for item_data in action_items_data:
                action_item = ActionItem(
                    meeting_id=meeting_id,
                    description=item_data.get('description', ''),
                    owner=item_data.get('owner'),
                    due_date=item_data.get('due_date'),
                    status=False
                )
                db.add(action_item)
                action_items.append(action_item)
            
            db.commit()
            for item in action_items:
                db.refresh(item)
            return action_items
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_action_item(self, action_item_id: int) -> Optional[ActionItem]:
        """Get an action item by ID"""
        db = self.get_db_session()
        try:
            return db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
        finally:
            db.close()
    
    def get_meeting_action_items(self, meeting_id: int) -> List[ActionItem]:
        """Get all action items for a meeting"""
        db = self.get_db_session()
        try:
            return db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).order_by(ActionItem.created_at).all()
        finally:
            db.close()
    
    def update_action_item_status(self, action_item_id: int, status: bool) -> Optional[ActionItem]:
        """Toggle action item status (Done/Not Done)"""
        db = self.get_db_session()
        try:
            action_item = db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
            if not action_item:
                return None
            
            action_item.status = status
            action_item.updated_at = datetime.now()
            db.commit()
            db.refresh(action_item)
            return action_item
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update_action_item(
        self, 
        action_item_id: int, 
        description: Optional[str] = None,
        owner: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[bool] = None
    ) -> Optional[ActionItem]:
        """Update an action item"""
        db = self.get_db_session()
        try:
            action_item = db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
            if not action_item:
                return None
            
            if description is not None:
                action_item.description = description
            if owner is not None:
                action_item.owner = owner
            if due_date is not None:
                action_item.due_date = due_date
            if status is not None:
                action_item.status = status
            
            action_item.updated_at = datetime.now()
            db.commit()
            db.refresh(action_item)
            return action_item
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def delete_action_item(self, action_item_id: int) -> bool:
        """Delete an action item"""
        db = self.get_db_session()
        try:
            action_item = db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
            if not action_item:
                return False
            
            db.delete(action_item)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    # Utility methods
    def get_meeting_with_action_items(self, meeting_id: int) -> Optional[Dict]:
        """Get meeting with all its action items"""
        db = self.get_db_session()
        try:
            meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
            if not meeting:
                return None
            
            action_items = db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).all()
            
            # Parse JSON fields
            decisions = json.loads(meeting.decisions) if meeting.decisions else []
            agenda_coverage = json.loads(meeting.agenda_coverage) if meeting.agenda_coverage else {}
            
            return {
                'meeting': {
                    'id': meeting.id,
                    'title': meeting.title,
                    'transcript': meeting.transcript,
                    'agenda': meeting.agenda,
                    'summary': meeting.summary,
                    'decisions': decisions,
                    'agenda_coverage': agenda_coverage,
                    'created_at': meeting.created_at.isoformat() if meeting.created_at else None,
                    'updated_at': meeting.updated_at.isoformat() if meeting.updated_at else None
                },
                'action_items': [
                    {
                        'id': item.id,
                        'description': item.description,
                        'owner': item.owner,
                        'due_date': item.due_date,
                        'status': item.status,
                        'created_at': item.created_at.isoformat() if item.created_at else None,
                        'updated_at': item.updated_at.isoformat() if item.updated_at else None
                    }
                    for item in action_items
                ]
            }
        finally:
            db.close()
    
    def get_action_items_summary(self) -> Dict:
        """Get summary of action items across all meetings"""
        db = self.get_db_session()
        try:
            total_items = db.query(ActionItem).count()
            completed_items = db.query(ActionItem).filter(ActionItem.status == True).count()
            pending_items = total_items - completed_items
            
            return {
                'total_action_items': total_items,
                'completed_action_items': completed_items,
                'pending_action_items': pending_items,
                'completion_rate': (completed_items / total_items * 100) if total_items > 0 else 0
            }
        finally:
            db.close()