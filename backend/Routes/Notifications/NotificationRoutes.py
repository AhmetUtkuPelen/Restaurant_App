"""
Notification Routes
API endpoints for push notifications and in-app notifications
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel

from database import get_db
from Services.NotificationService import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])

# Pydantic models
class NotificationCreate(BaseModel):
    title: str
    message: str
    notification_type: str
    data: Dict = {}

@router.get("/user/{user_id}")
async def get_user_notifications(
    user_id: str,
    unread_only: bool = Query(False, description="Get only unread notifications"),
    limit: int = Query(50, description="Number of notifications to return"),
    db: Session = Depends(get_db)
):
    """Get notifications for a user"""
    
    try:
        notifications = NotificationService.get_user_notifications(
            db=db,
            user_id=user_id,
            unread_only=unread_only,
            limit=limit
        )
        
        return {
            "success": True,
            "user_id": user_id,
            "unread_only": unread_only,
            "notifications": notifications,
            "count": len(notifications)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notifications: {str(e)}"
        )

@router.post("/create")
async def create_notification(
    notification_data: NotificationCreate,
    user_id: str,  # Target user ID
    db: Session = Depends(get_db)
):
    """Create a new notification"""
    
    try:
        notification = NotificationService.create_notification(
            db=db,
            user_id=user_id,
            title=notification_data.title,
            message=notification_data.message,
            notification_type=notification_data.notification_type,
            data=notification_data.data
        )
        
        return {
            "success": True,
            "notification": {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "notification_type": notification.notification_type,
                "created_at": notification.created_at.isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create notification: {str(e)}"
        )

@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    
    try:
        success = NotificationService.mark_as_read(db, notification_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found or access denied"
            )
        
        return {
            "success": True,
            "message": "Notification marked as read"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark notification as read: {str(e)}"
        )

@router.put("/user/{user_id}/read-all")
async def mark_all_notifications_as_read(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for a user"""
    
    try:
        updated_count = NotificationService.mark_all_as_read(db, user_id)
        
        return {
            "success": True,
            "updated_count": updated_count,
            "message": f"Marked {updated_count} notifications as read"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark all notifications as read: {str(e)}"
        )

@router.get("/user/{user_id}/unread-count")
async def get_unread_count(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get count of unread notifications for a user"""
    
    try:
        count = NotificationService.get_unread_count(db, user_id)
        
        return {
            "success": True,
            "user_id": user_id,
            "unread_count": count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get unread count: {str(e)}"
        )

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Delete a notification"""
    
    try:
        success = NotificationService.delete_notification(db, notification_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found or access denied"
            )
        
        return {
            "success": True,
            "message": "Notification deleted"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete notification: {str(e)}"
        )

@router.get("/user/{user_id}/stats")
async def get_notification_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get notification statistics for a user"""
    
    try:
        stats = NotificationService.get_notification_stats(db, user_id)
        
        return {
            "success": True,
            "user_id": user_id,
            "stats": stats
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notification stats: {str(e)}"
        )

@router.post("/send-message-notification")
async def send_message_notification(
    recipient_id: str,
    sender_name: str,
    message_content: str,
    room_name: str = None,
    db: Session = Depends(get_db)
):
    """Send notification for new message"""
    
    try:
        NotificationService.send_message_notification(
            db=db,
            recipient_id=recipient_id,
            sender_name=sender_name,
            message_content=message_content,
            room_name=room_name
        )
        
        return {
            "success": True,
            "message": "Message notification sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message notification: {str(e)}"
        )

@router.post("/send-mention-notification")
async def send_mention_notification(
    mentioned_user_id: str,
    sender_name: str,
    message_content: str,
    room_name: str = None,
    db: Session = Depends(get_db)
):
    """Send notification for user mention"""
    
    try:
        NotificationService.send_mention_notification(
            db=db,
            mentioned_user_id=mentioned_user_id,
            sender_name=sender_name,
            message_content=message_content,
            room_name=room_name
        )
        
        return {
            "success": True,
            "message": "Mention notification sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send mention notification: {str(e)}"
        )

@router.post("/send-room-invite-notification")
async def send_room_invite_notification(
    invited_user_id: str,
    inviter_name: str,
    room_name: str,
    room_id: str,
    db: Session = Depends(get_db)
):
    """Send notification for room invitation"""
    
    try:
        NotificationService.send_room_invite_notification(
            db=db,
            invited_user_id=invited_user_id,
            inviter_name=inviter_name,
            room_name=room_name,
            room_id=room_id
        )
        
        return {
            "success": True,
            "message": "Room invite notification sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send room invite notification: {str(e)}"
        )

@router.delete("/cleanup")
async def cleanup_old_notifications(
    days_old: int = Query(30, description="Delete notifications older than this many days"),
    db: Session = Depends(get_db)
):
    """Clean up old notifications"""
    
    try:
        deleted_count = NotificationService.cleanup_old_notifications(db, days_old)
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Deleted {deleted_count} notifications older than {days_old} days"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cleanup notifications: {str(e)}"
        )
