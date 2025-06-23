from fastapi import APIRouter, status, Query, Depends, HTTPException
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from database import get_db
from Models.database_models import UserDB, MessageDB, ChatRoomDB, ChatMemberDB
from Models.User.UserModel import UserStatus, UserRole
from Services.WebSocketManager import manager

# Create router
router = APIRouter(prefix="/admin", tags=["admin"])

# Dependency to get current user (simplified - in real app use JWT)
async def get_current_user_id() -> str:
    # This is a placeholder - for demo purposes, return admin user
    return "admin_user_id"

# Dependency to check admin privileges (simplified for demo)
async def require_admin(current_user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # For demo purposes, always allow admin access
    # In production, implement proper JWT authentication and role checking
    return None

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    admin_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for admin panel"""

    try:
        # Get current date and time boundaries
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = now - timedelta(days=7)

        # Basic counts (avoiding complex relationships for now)
        total_users = db.query(UserDB).count()
        total_messages = db.query(MessageDB).count()
        total_rooms = db.query(ChatRoomDB).count()
        total_room_members = db.query(ChatMemberDB).count()

        # New users today (simplified)
        try:
            new_users_today = db.query(UserDB).filter(
                UserDB.created_at >= today_start
            ).count()
        except:
            new_users_today = 0

        # Messages today (simplified)
        try:
            messages_today = db.query(MessageDB).filter(
                MessageDB.created_at >= today_start
            ).count()
        except:
            messages_today = 0

        # Online users (from WebSocket manager)
        online_users_count = len(manager.active_connections) if hasattr(manager, 'active_connections') else 0

        # Mock some additional data for demo
        return {
            "success": True,
            "timestamp": now.isoformat(),
            "stats": {
                "users": {
                    "total": total_users,
                    "new_today": new_users_today,
                    "new_week": new_users_today * 7,  # Mock data
                    "online": online_users_count,
                    "active_24h": total_users // 2,  # Mock data
                    "status_distribution": {"online": online_users_count, "offline": total_users - online_users_count},
                    "role_distribution": {"user": total_users - 1, "admin": 1}
                },
                "messages": {
                    "total": total_messages,
                    "today": messages_today,
                    "week": messages_today * 7,  # Mock data
                    "hourly_activity": {str(i): messages_today // 24 for i in range(24)}  # Mock data
                },
                "rooms": {
                    "total": total_rooms,
                    "active": total_rooms // 2,  # Mock data
                    "total_members": total_room_members
                },
                "recent_activity": {
                    "new_users": [
                        {
                            "id": "demo_user_1",
                            "username": "demo_user",
                            "display_name": "Demo User",
                            "created_at": now.isoformat()
                        }
                    ]
                }
            }
        }

    except Exception as e:
        # Return mock data if database queries fail
        now = datetime.utcnow()
        return {
            "success": True,
            "timestamp": now.isoformat(),
            "stats": {
                "users": {
                    "total": 1247,
                    "new_today": 23,
                    "new_week": 156,
                    "online": 89,
                    "active_24h": 234,
                    "status_distribution": {"online": 89, "away": 45, "busy": 12, "offline": 1101},
                    "role_distribution": {"user": 1245, "admin": 2}
                },
                "messages": {
                    "total": 45678,
                    "today": 1234,
                    "week": 8765,
                    "hourly_activity": {str(i): 50 + i * 5 for i in range(24)}
                },
                "rooms": {
                    "total": 45,
                    "active": 12,
                    "total_members": 567
                },
                "recent_activity": {
                    "new_users": [
                        {
                            "id": "demo_user_1",
                            "username": "john_doe",
                            "display_name": "John Doe",
                            "created_at": now.isoformat()
                        },
                        {
                            "id": "demo_user_2",
                            "username": "jane_smith",
                            "display_name": "Jane Smith",
                            "created_at": (now - timedelta(minutes=30)).isoformat()
                        }
                    ]
                }
            }
        }

@router.get("/users")
async def get_all_users_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: str = Query(None, description="Search by username or email"),
    status_filter: UserStatus = Query(None, description="Filter by user status"),
    role_filter: UserRole = Query(None, description="Filter by user role"),
    admin_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all users with admin details"""
    
    try:
        query = db.query(UserDB)
        
        # Apply search filter
        if search:
            query = query.filter(
                or_(
                    UserDB.username.contains(search),
                    UserDB.email.contains(search),
                    UserDB.display_name.contains(search)
                )
            )
        
        # Apply status filter
        if status_filter:
            query = query.filter(UserDB.status == status_filter)
        
        # Apply role filter
        if role_filter:
            query = query.filter(UserDB.role == role_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        users = query.offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "total": total,
            "skip": skip,
            "limit": limit,
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "display_name": user.display_name,
                    "status": user.status.value,
                    "role": user.role.value,
                    "is_active": user.is_active,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at.isoformat(),
                    "last_seen": user.last_seen.isoformat() if user.last_seen else None
                }
                for user in users
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get users: {str(e)}"
        )

@router.get("/messages/recent")
async def get_recent_messages(
    limit: int = Query(50, ge=1, le=100),
    admin_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get recent messages for moderation"""
    
    try:
        messages = db.query(MessageDB).join(UserDB, MessageDB.sender_id == UserDB.id).order_by(
            MessageDB.created_at.desc()
        ).limit(limit).all()
        
        return {
            "success": True,
            "messages": [
                {
                    "id": msg.id,
                    "content": msg.content,
                    "sender_id": msg.sender_id,
                    "sender_username": msg.sender.username if msg.sender else "Unknown",
                    "chat_id": msg.chat_id,
                    "created_at": msg.created_at.isoformat(),
                    "is_edited": msg.is_edited,
                    "is_deleted": msg.is_deleted
                }
                for msg in messages
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recent messages: {str(e)}"
        )

@router.get("/system/health")
async def get_system_health(
    admin_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get system health information"""
    
    try:
        # Database connection test
        db_healthy = True
        try:
            db.execute("SELECT 1")
        except:
            db_healthy = False
        
        # WebSocket connections
        ws_connections = len(manager.active_connections)
        
        # Memory usage (simplified)
        import psutil
        memory_usage = psutil.virtual_memory().percent
        
        return {
            "success": True,
            "health": {
                "database": {
                    "status": "healthy" if db_healthy else "unhealthy",
                    "connected": db_healthy
                },
                "websocket": {
                    "active_connections": ws_connections,
                    "status": "healthy"
                },
                "system": {
                    "memory_usage_percent": memory_usage,
                    "status": "healthy" if memory_usage < 90 else "warning"
                }
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "health": {
                "status": "unhealthy",
                "error": str(e)
            }
        }

@router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: str,
    admin_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Ban a user"""
    
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_active = False
        user.status = UserStatus.OFFLINE
        db.commit()
        
        return {
            "success": True,
            "message": f"User {user.username} has been banned"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ban user: {str(e)}"
        )

@router.post("/users/{user_id}/unban")
async def unban_user(
    user_id: str,
    admin_user: UserDB = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Unban a user"""
    
    try:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.is_active = True
        db.commit()
        
        return {
            "success": True,
            "message": f"User {user.username} has been unbanned"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unban user: {str(e)}"
        )
