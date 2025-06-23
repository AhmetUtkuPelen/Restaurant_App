"""
Call Service for handling voice and video calling functionality
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from Models.database_models import CallSessionDB, CallParticipantDB, UserDB, ChatRoomDB
from Services.WebSocketManager import manager
from Services.NotificationService import NotificationService
from datetime import datetime, timedelta
import uuid
import json


class CallService:
    
    @staticmethod
    async def initiate_call(
        db: Session,
        caller_id: str,
        call_type: str,  # "audio" or "video"
        room_id: str = None,
        participant_ids: List[str] = None
    ) -> CallSessionDB:
        """Initiate a new call session"""
        
        call = CallSessionDB(
            id=str(uuid.uuid4()),
            caller_id=caller_id,
            call_type=call_type,
            room_id=room_id,
            status="initiated"
        )
        
        # Add call to database
        db.add(call)
        db.commit()
        db.refresh(call)
        
        # Add caller as participant
        caller_participant = CallParticipantDB(
            id=str(uuid.uuid4()),
            call_id=call.id,
            user_id=caller_id,
            status="joined"
        )
        db.add(caller_participant)
        
        # Add other participants
        if participant_ids:
            for participant_id in participant_ids:
                if participant_id != caller_id:  # Don't add caller twice
                    participant = CallParticipantDB(
                        id=str(uuid.uuid4()),
                        call_id=call.id,
                        user_id=participant_id,
                        status="invited"
                    )
                    db.add(participant)
        
        db.commit()
        
        # Send call invitations
        CallService.send_call_invitations(db, call)
        
        return call


    @staticmethod
    async def send_call_invitations(db: Session, call: CallSessionDB):
        """Send call invitations to users"""
        
        # Get caller info
        caller = db.query(UserDB).filter(UserDB.id == call.caller_id).first()
        caller_name = caller.display_name if caller else "Unknown"
        
        # Get all invited participants
        participants = db.query(CallParticipantDB).filter(
            CallParticipantDB.call_id == call.id,
            CallParticipantDB.status == "invited"
        ).all()
        
        for participant in participants:
            # Send WebSocket notification to user
            if manager.is_user_online(participant.user_id):
                call_data = {
                    "type": "call_invitation",
                    "call_id": call.id,
                    "caller_id": call.caller_id,
                    "caller_name": caller_name,
                    "call_type": call.call_type,
                    "room_id": call.room_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                import asyncio
                asyncio.create_task(
                    manager.send_personal_json(call_data, participant.user_id)
                )
            
            # Send push notification
            NotificationService.send_call_notification(
                db=db,
                recipient_id=participant.user_id,
                caller_name=caller_name,
                call_type=call.call_type,
                call_id=call.id
            )
    
    @staticmethod
    async def join_call(db: Session, call_id: str, user_id: str) -> bool:
        """Join an existing call"""
        
        # Check if call exists and is active
        call = db.query(CallSessionDB).filter(
            CallSessionDB.id == call_id,
            CallSessionDB.status.in_(["initiated", "ringing", "active"])
        ).first()
        
        # Check if call exists and is active
        if not call:
            return False
        
        # Check if user is invited
        participant = db.query(CallParticipantDB).filter(
            CallParticipantDB.call_id == call_id,
            CallParticipantDB.user_id == user_id
        ).first()
        
        if not participant:
            return False
        
        # Update participant status
        participant.status = "joined"
        participant.joined_at = datetime.utcnow()
        
        # Update call status to active if not already
        if call.status != "active":
            call.status = "active"
        
        db.commit()
        
        # Notify other participants
        CallService.notify_call_participants(db, call_id, "user_joined", {
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return True
    

    @staticmethod
    async def leave_call(db: Session, call_id: str, user_id: str) -> bool:
        """Leave a call"""
        
        participant = db.query(CallParticipantDB).filter(
            CallParticipantDB.call_id == call_id,
            CallParticipantDB.user_id == user_id
        ).first()
        
        if not participant:
            return False
        
        participant.status = "left"
        participant.left_at = datetime.utcnow()
        
        # Check if this was the last participant
        active_participants = db.query(CallParticipantDB).filter(
            CallParticipantDB.call_id == call_id,
            CallParticipantDB.status == "joined"
        ).count()
        
        if active_participants <= 1:  # Only caller or no one left
            # End the call
            call = db.query(CallSessionDB).filter(CallSessionDB.id == call_id).first()
            if call:
                call.status = "ended"
                call.ended_at = datetime.utcnow()
                
                # Calculate duration
                if call.started_at:
                    duration = (call.ended_at - call.started_at).total_seconds()
                    call.duration = int(duration)
        
        db.commit()
        
        # Notify other participants
        CallService.notify_call_participants(db, call_id, "user_left", {
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return True
    
    @staticmethod
    async def reject_call(db: Session, call_id: str, user_id: str) -> bool:
        """Reject a call invitation"""
        
        participant = db.query(CallParticipantDB).filter(
            CallParticipantDB.call_id == call_id,
            CallParticipantDB.user_id == user_id,
            CallParticipantDB.status == "invited"
        ).first()
        
        if not participant:
            return False
        
        participant.status = "rejected"
        db.commit()
        
        # Notify caller
        call = db.query(CallSessionDB).filter(CallSessionDB.id == call_id).first()
        if call and manager.is_user_online(call.caller_id):
            rejection_data = {
                "type": "call_rejected",
                "call_id": call_id,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            import asyncio
            asyncio.create_task(
                manager.send_personal_json(rejection_data, call.caller_id)
            )
        
        return True
    
    @staticmethod
    async def end_call(db: Session, call_id: str, user_id: str) -> bool:
        """End a call (only caller or admin can end)"""
        
        call = db.query(CallSessionDB).filter(CallSessionDB.id == call_id).first()
        if not call:
            return False
        
        # Check if user has permission to end call
        if call.caller_id != user_id:
            # Check if user is admin of the room
            if call.room_id:
                from Models.database_models import ChatMemberDB
                member = db.query(ChatMemberDB).filter(
                    ChatMemberDB.chat_id == call.room_id,
                    ChatMemberDB.user_id == user_id,
                    ChatMemberDB.is_admin == True
                ).first()
                if not member:
                    return False
            else:
                return False
        
        # End the call
        call.status = "ended"
        call.ended_at = datetime.utcnow()
        
        # Calculate duration
        if call.started_at:
            duration = (call.ended_at - call.started_at).total_seconds()
            call.duration = int(duration)
        
        # Update all active participants
        db.query(CallParticipantDB).filter(
            CallParticipantDB.call_id == call_id,
            CallParticipantDB.status == "joined"
        ).update({
            "status": "left",
            "left_at": datetime.utcnow()
        })
        
        db.commit()
        
        # Notify all participants
        CallService.notify_call_participants(db, call_id, "call_ended", {
            "ended_by": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return True
    
    @staticmethod
    async def notify_call_participants(db: Session, call_id: str, event_type: str, data: Dict):
        """Send notifications to all call participants"""
        
        participants = db.query(CallParticipantDB).filter(
            CallParticipantDB.call_id == call_id,
            CallParticipantDB.status.in_(["joined", "invited"])
        ).all()
        
        notification_data = {
            "type": event_type,
            "call_id": call_id,
            **data
        }
        
        for participant in participants:
            if manager.is_user_online(participant.user_id):
                import asyncio
                asyncio.create_task(
                    manager.send_personal_json(notification_data, participant.user_id)
                )
    
    @staticmethod
    async def get_active_calls(db: Session, user_id: str) -> List[Dict]:
        """Get active calls for a user"""
        
        calls = db.query(CallSessionDB).join(CallParticipantDB).filter(
            CallParticipantDB.user_id == user_id,
            CallSessionDB.status.in_(["initiated", "ringing", "active"]),
            CallParticipantDB.status.in_(["invited", "joined"])
        ).all()
        
        result = []
        for call in calls:
            # Get caller info
            caller = db.query(UserDB).filter(UserDB.id == call.caller_id).first()
            
            # Get participants
            participants = db.query(CallParticipantDB, UserDB).join(
                UserDB, CallParticipantDB.user_id == UserDB.id
            ).filter(CallParticipantDB.call_id == call.id).all()
            
            participant_list = []
            for participant, user in participants:
                participant_list.append({
                    "user_id": user.id,
                    "username": user.username,
                    "display_name": user.display_name,
                    "status": participant.status,
                    "joined_at": participant.joined_at
                })
            
            # Get room info if applicable
            room = None
            if call.room_id:
                room = db.query(ChatRoomDB).filter(ChatRoomDB.id == call.room_id).first()
            
            result.append({
                "id": call.id,
                "call_type": call.call_type,
                "status": call.status,
                "started_at": call.started_at,
                "caller": {
                    "id": caller.id,
                    "username": caller.username,
                    "display_name": caller.display_name
                } if caller else None,
                "room": {
                    "id": room.id,
                    "name": room.name
                } if room else None,
                "participants": participant_list
            })
        
        return result
    
    @staticmethod
    async def get_call_history(db: Session, user_id: str, limit: int = 50) -> List[Dict]:
        """Get call history for a user"""
        
        calls = db.query(CallSessionDB).join(CallParticipantDB).filter(
            CallParticipantDB.user_id == user_id,
            CallSessionDB.status == "ended"
        ).order_by(CallSessionDB.started_at.desc()).limit(limit).all()
        
        result = []
        for call in calls:
            caller = db.query(UserDB).filter(UserDB.id == call.caller_id).first()
            
            result.append({
                "id": call.id,
                "call_type": call.call_type,
                "started_at": call.started_at,
                "ended_at": call.ended_at,
                "duration": call.duration,
                "caller": {
                    "id": caller.id,
                    "username": caller.username,
                    "display_name": caller.display_name
                } if caller else None
            })
        
        return result
