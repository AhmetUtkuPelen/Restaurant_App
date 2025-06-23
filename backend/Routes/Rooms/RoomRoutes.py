"""
Chat Room Routes
API endpoints for chat rooms/channels
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel

from database import get_db
from Services.RoomService import RoomService
from Services.NotificationService import NotificationService
from Services.WebSocketManager import manager

router = APIRouter(prefix="/rooms", tags=["rooms"])

# Pydantic models
class RoomCreate(BaseModel):
    name: str
    description: str = ""
    is_private: bool = False

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_private: Optional[bool] = None

class RoomResponse(BaseModel):
    id: str
    name: str
    description: str
    is_private: bool
    created_by: str
    created_at: str
    member_count: int

@router.post("/create", response_model=Dict)
async def create_room(
    room_data: RoomCreate,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Create a new chat room"""
    
    try:
        room = RoomService.create_room(
            db=db,
            name=room_data.name,
            description=room_data.description,
            created_by=user_id,
            is_private=room_data.is_private
        )
        
        # Broadcast room creation to all users (for public rooms)
        if not room_data.is_private:
            room_created = {
                "type": "room_created",
                "room": {
                    "id": room.id,
                    "name": room.name,
                    "description": room.description,
                    "created_by": room.created_by,
                    "created_at": room.created_at.isoformat(),
                    "member_count": 1
                }
            }
            await manager.broadcast_json(room_created)
        
        return {
            "success": True,
            "room": {
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "is_private": room.is_private,
                "created_by": room.created_by,
                "created_at": room.created_at.isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create room: {str(e)}"
        )

@router.get("/user/{user_id}")
async def get_user_rooms(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all rooms that a user is a member of"""
    
    try:
        rooms = RoomService.get_user_rooms(db, user_id)
        return {
            "user_id": user_id,
            "rooms": rooms
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user rooms: {str(e)}"
        )

@router.get("/public")
async def get_public_rooms(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all public rooms"""
    
    try:
        rooms = RoomService.get_public_rooms(db, limit)
        return {
            "public_rooms": rooms
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get public rooms: {str(e)}"
        )

@router.post("/{room_id}/join")
async def join_room(
    room_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Join a chat room"""
    
    try:
        success = RoomService.join_room(db, room_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to join room. Room may not exist or user is already a member."
            )
        
        # Get room info
        room = RoomService.get_room_by_id(db, room_id)
        
        # Broadcast user joined to room members
        user_joined = {
            "type": "user_joined_room",
            "room_id": room_id,
            "user_id": user_id,
            "room_name": room.name if room else "Unknown"
        }
        
        # Send to all room members
        await manager.broadcast_to_room(user_joined, room_id)
        
        return {
            "success": True,
            "message": f"Successfully joined room: {room.name if room else room_id}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to join room: {str(e)}"
        )

@router.post("/{room_id}/leave")
async def leave_room(
    room_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Leave a chat room"""
    
    try:
        success = RoomService.leave_room(db, room_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to leave room. User may not be a member."
            )
        
        # Broadcast user left to room members
        user_left = {
            "type": "user_left_room",
            "room_id": room_id,
            "user_id": user_id
        }
        
        await manager.broadcast_to_room(user_left, room_id)
        
        return {
            "success": True,
            "message": "Successfully left room"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to leave room: {str(e)}"
        )

@router.get("/{room_id}/members")
async def get_room_members(
    room_id: str,
    db: Session = Depends(get_db)
):
    """Get all members of a room"""
    
    try:
        members = RoomService.get_room_members(db, room_id)
        return {
            "room_id": room_id,
            "members": members
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get room members: {str(e)}"
        )

@router.get("/{room_id}")
async def get_room_details(
    room_id: str,
    db: Session = Depends(get_db)
):
    """Get room details"""
    
    try:
        room = RoomService.get_room_by_id(db, room_id)
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )
        
        members = RoomService.get_room_members(db, room_id)
        
        return {
            "id": room.id,
            "name": room.name,
            "description": room.description,
            "is_private": room.is_private,
            "created_by": room.created_by,
            "created_at": room.created_at.isoformat(),
            "member_count": len(members),
            "members": members
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get room details: {str(e)}"
        )

@router.put("/{room_id}")
async def update_room(
    room_id: str,
    room_data: RoomUpdate,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Update room details (admin only)"""
    
    try:
        updates = room_data.dict(exclude_unset=True)
        
        room = RoomService.update_room(db, room_id, user_id, **updates)
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only room admins can update room details"
            )
        
        # Broadcast room update to members
        room_updated = {
            "type": "room_updated",
            "room_id": room_id,
            "updates": updates,
            "updated_by": user_id
        }
        
        await manager.broadcast_to_room(room_updated, room_id)
        
        return {
            "success": True,
            "room": {
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "is_private": room.is_private
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update room: {str(e)}"
        )

@router.post("/{room_id}/promote/{target_user_id}")
async def promote_to_admin(
    room_id: str,
    target_user_id: str,
    admin_user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Promote a user to admin"""
    
    try:
        success = RoomService.promote_to_admin(db, room_id, admin_user_id, target_user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only room admins can promote users"
            )
        
        # Broadcast promotion to room members
        promotion = {
            "type": "user_promoted",
            "room_id": room_id,
            "user_id": target_user_id,
            "promoted_by": admin_user_id
        }
        
        await manager.broadcast_to_room(promotion, room_id)
        
        return {
            "success": True,
            "message": "User promoted to admin"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to promote user: {str(e)}"
        )

@router.get("/search")
async def search_rooms(
    query: str,
    user_id: str = None,
    db: Session = Depends(get_db)
):
    """Search for rooms"""
    
    try:
        rooms = RoomService.search_rooms(db, query, user_id)
        return {
            "query": query,
            "results": rooms
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search rooms: {str(e)}"
        )
