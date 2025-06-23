from fastapi import APIRouter, status, Query, Depends
from typing import List
from sqlalchemy.orm import Session
from Controllers.Message.MessageController import MessageController
from Schemas.Message.MessageSchemas import (
    MessageCreate, MessageUpdate, MessageResponse
)
from database import get_db

# Create router
router = APIRouter(prefix="/messages", tags=["messages"])

# Initialize controller
message_controller = MessageController()

# Dependency to get current user (simplified - in real app use JWT)
async def get_current_user_id() -> str:
    # This is a placeholder - implement proper authentication
    return "current_user_id"

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_data: MessageCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new message"""
    return await message_controller.create_message(db, current_user_id, message_data)

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message_by_id(message_id: str, db: Session = Depends(get_db)):
    """Get message by ID"""
    return await message_controller.get_message_by_id(db, message_id)

@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: str,
    update_data: MessageUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update a message (only sender can edit)"""
    return await message_controller.update_message(db, message_id, current_user_id, update_data)

@router.delete("/{message_id}")
async def delete_message(
    message_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete a message (only sender can delete)"""
    return await message_controller.delete_message(db, message_id, current_user_id)

@router.get("/conversation/{user_id}", response_model=List[MessageResponse])
async def get_conversation_messages(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get messages between current user and another user"""
    return await message_controller.get_conversation_messages(
        db, current_user_id, user_id, skip, limit
    )

@router.get("/chat/{chat_id}", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get messages for a specific chat/group"""
    return await message_controller.get_chat_messages(db, chat_id, skip, limit)

@router.post("/{message_id}/reactions", response_model=MessageResponse)
async def add_reaction(
    message_id: str,
    emoji: str = Query(..., min_length=1, max_length=10),
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Add a reaction to a message"""
    return await message_controller.add_reaction(db, message_id, current_user_id, emoji)

@router.delete("/{message_id}/reactions")
async def remove_reaction(
    message_id: str,
    emoji: str = Query(..., min_length=1, max_length=10),
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Remove a reaction from a message"""
    return await message_controller.remove_reaction(db, message_id, current_user_id, emoji)

@router.patch("/{message_id}/read", response_model=MessageResponse)
async def mark_message_as_read(
    message_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Mark a message as read"""
    return await message_controller.mark_message_as_read(db, message_id, current_user_id)