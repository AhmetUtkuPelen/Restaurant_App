"""
Notification Service
Handles push notifications and in-app notifications
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from Models.database_models import NotificationDB, UserDB
from Services.WebSocketManager import manager
from datetime import datetime
import uuid
import json

class NotificationService:
    
    @staticmethod
    def create_notification(
        db: Session, 
        user_id: str, 
        title: str, 
        message: str, 
        notification_type: str,
        data: Dict = None
    ) -> NotificationDB:
        """Create a new notification"""
        
        notification = NotificationDB(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            data=data or {}
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        # Send real-time notification if user is online
        NotificationService.send_realtime_notification(notification)
        
        return notification
    
    @staticmethod
    def send_realtime_notification(notification: NotificationDB):
        """Send real-time notification via WebSocket"""
        
        if manager.is_user_online(notification.user_id):
            notification_data = {
                "type": "notification",
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "notification_type": notification.notification_type,
                "data": notification.data,
                "created_at": notification.created_at.isoformat(),
                "is_read": notification.is_read
            }
            
            # Send to user via WebSocket
            import asyncio
            asyncio.create_task(
                manager.send_personal_json(notification_data, notification.user_id)
            )
    
    @staticmethod
    def get_user_notifications(
        db: Session, 
        user_id: str, 
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict]:
        """Get notifications for a user"""
        
        query = db.query(NotificationDB).filter(NotificationDB.user_id == user_id)
        
        if unread_only:
            query = query.filter(NotificationDB.is_read == False)
        
        notifications = query.order_by(
            NotificationDB.created_at.desc()
        ).limit(limit).all()
        
        return [
            {
                "id": notif.id,
                "title": notif.title,
                "message": notif.message,
                "notification_type": notif.notification_type,
                "data": notif.data,
                "is_read": notif.is_read,
                "created_at": notif.created_at
            }
            for notif in notifications
        ]
    
    @staticmethod
    def mark_as_read(db: Session, notification_id: str, user_id: str) -> bool:
        """Mark a notification as read"""
        
        notification = db.query(NotificationDB).filter(
            NotificationDB.id == notification_id,
            NotificationDB.user_id == user_id
        ).first()
        
        if notification:
            notification.is_read = True
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def mark_all_as_read(db: Session, user_id: str) -> int:
        """Mark all notifications as read for a user"""
        
        updated_count = db.query(NotificationDB).filter(
            NotificationDB.user_id == user_id,
            NotificationDB.is_read == False
        ).update({"is_read": True})
        
        db.commit()
        return updated_count
    
    @staticmethod
    def get_unread_count(db: Session, user_id: str) -> int:
        """Get count of unread notifications for a user"""
        
        return db.query(NotificationDB).filter(
            NotificationDB.user_id == user_id,
            NotificationDB.is_read == False
        ).count()
    
    @staticmethod
    def delete_notification(db: Session, notification_id: str, user_id: str) -> bool:
        """Delete a notification"""
        
        notification = db.query(NotificationDB).filter(
            NotificationDB.id == notification_id,
            NotificationDB.user_id == user_id
        ).first()
        
        if notification:
            db.delete(notification)
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def send_message_notification(
        db: Session,
        recipient_id: str,
        sender_name: str,
        message_content: str,
        room_name: str = None
    ):
        """Send notification for new message"""
        
        if room_name:
            title = f"New message in {room_name}"
            message = f"{sender_name}: {message_content[:100]}..."
        else:
            title = f"New message from {sender_name}"
            message = message_content[:100] + "..." if len(message_content) > 100 else message_content
        
        NotificationService.create_notification(
            db=db,
            user_id=recipient_id,
            title=title,
            message=message,
            notification_type="message",
            data={
                "sender_name": sender_name,
                "room_name": room_name,
                "message_preview": message_content[:100]
            }
        )
    
    @staticmethod
    def send_mention_notification(
        db: Session,
        mentioned_user_id: str,
        sender_name: str,
        message_content: str,
        room_name: str = None
    ):
        """Send notification for user mention"""
        
        title = f"You were mentioned by {sender_name}"
        if room_name:
            title += f" in {room_name}"
        
        message = message_content[:100] + "..." if len(message_content) > 100 else message_content
        
        NotificationService.create_notification(
            db=db,
            user_id=mentioned_user_id,
            title=title,
            message=message,
            notification_type="mention",
            data={
                "sender_name": sender_name,
                "room_name": room_name,
                "message_content": message_content
            }
        )
    
    @staticmethod
    def send_room_invite_notification(
        db: Session,
        invited_user_id: str,
        inviter_name: str,
        room_name: str,
        room_id: str
    ):
        """Send notification for room invitation"""
        
        title = f"Room invitation from {inviter_name}"
        message = f"You've been invited to join '{room_name}'"
        
        NotificationService.create_notification(
            db=db,
            user_id=invited_user_id,
            title=title,
            message=message,
            notification_type="room_invite",
            data={
                "inviter_name": inviter_name,
                "room_name": room_name,
                "room_id": room_id
            }
        )
    
    @staticmethod
    def send_call_notification(
        db: Session,
        recipient_id: str,
        caller_name: str,
        call_type: str,
        call_id: str
    ):
        """Send notification for incoming call"""
        
        title = f"Incoming {call_type} call"
        message = f"{caller_name} is calling you"
        
        NotificationService.create_notification(
            db=db,
            user_id=recipient_id,
            title=title,
            message=message,
            notification_type="call",
            data={
                "caller_name": caller_name,
                "call_type": call_type,
                "call_id": call_id
            }
        )
    
    @staticmethod
    def send_reaction_notification(
        db: Session,
        message_author_id: str,
        reactor_name: str,
        emoji: str,
        message_content: str
    ):
        """Send notification for message reaction"""
        
        title = f"{reactor_name} reacted to your message"
        message = f"Reacted with {emoji} to: {message_content[:50]}..."
        
        NotificationService.create_notification(
            db=db,
            user_id=message_author_id,
            title=title,
            message=message,
            notification_type="reaction",
            data={
                "reactor_name": reactor_name,
                "emoji": emoji,
                "message_preview": message_content[:100]
            }
        )
    
    @staticmethod
    def cleanup_old_notifications(db: Session, days_old: int = 30) -> int:
        """Clean up old notifications"""
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        deleted_count = db.query(NotificationDB).filter(
            NotificationDB.created_at < cutoff_date
        ).delete()
        
        db.commit()
        return deleted_count
    
    @staticmethod
    def get_notification_stats(db: Session, user_id: str) -> Dict:
        """Get notification statistics for a user"""
        
        total_notifications = db.query(NotificationDB).filter(
            NotificationDB.user_id == user_id
        ).count()
        
        unread_notifications = db.query(NotificationDB).filter(
            NotificationDB.user_id == user_id,
            NotificationDB.is_read == False
        ).count()
        
        # Get counts by type
        from sqlalchemy import func
        type_counts = db.query(
            NotificationDB.notification_type,
            func.count(NotificationDB.id).label('count')
        ).filter(
            NotificationDB.user_id == user_id
        ).group_by(NotificationDB.notification_type).all()
        
        type_stats = {type_count.notification_type: type_count.count for type_count in type_counts}
        
        return {
            "total_notifications": total_notifications,
            "unread_notifications": unread_notifications,
            "read_notifications": total_notifications - unread_notifications,
            "types": type_stats
        }
