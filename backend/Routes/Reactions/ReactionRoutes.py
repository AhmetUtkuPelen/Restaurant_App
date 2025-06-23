"""
Message Reaction Routes
API endpoints for emoji reactions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel

from database import get_db
from Services.ReactionService import ReactionService
from Services.NotificationService import NotificationService
from Services.WebSocketManager import manager
from Models.database_models import MessageDB, UserDB

router = APIRouter(prefix="/reactions", tags=["reactions"])

# Pydantic models
class ReactionCreate(BaseModel):
    message_id: str
    emoji: str
    emoji_name: str = None

class ReactionResponse(BaseModel):
    id: str
    message_id: str
    user_id: str
    emoji: str
    emoji_name: str = None
    created_at: str

@router.post("/add", response_model=Dict)
async def add_reaction(
    reaction_data: ReactionCreate,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Add or toggle a reaction to a message"""
    
    try:
        # Check if message exists
        message = db.query(MessageDB).filter(MessageDB.id == reaction_data.message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Add reaction (will toggle if already exists)
        reaction = ReactionService.add_reaction(
            db=db,
            message_id=reaction_data.message_id,
            user_id=user_id,
            emoji=reaction_data.emoji,
            emoji_name=reaction_data.emoji_name
        )
        
        # Get updated reactions for the message
        reactions = ReactionService.get_message_reactions(db, reaction_data.message_id)
        
        # Send real-time update to all users
        reaction_update = {
            "type": "reaction_update",
            "message_id": reaction_data.message_id,
            "reactions": reactions,
            "user_id": user_id,
            "action": "added" if reaction else "removed",
            "emoji": reaction_data.emoji
        }
        
        await manager.broadcast_json(reaction_update)
        
        # Send notification to message author (if not reacting to own message)
        if message.sender_id != user_id and reaction:
            user = db.query(UserDB).filter(UserDB.id == user_id).first()
            user_name = user.display_name if user else "Someone"
            
            NotificationService.send_reaction_notification(
                db=db,
                message_author_id=message.sender_id,
                reactor_name=user_name,
                emoji=reaction_data.emoji,
                message_content=message.content
            )
        
        return {
            "success": True,
            "action": "added" if reaction else "removed",
            "reactions": reactions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add reaction: {str(e)}"
        )

@router.delete("/remove")
async def remove_reaction(
    message_id: str,
    emoji: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Remove a specific reaction"""
    
    try:
        success = ReactionService.remove_reaction(
            db=db,
            message_id=message_id,
            user_id=user_id,
            emoji=emoji
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reaction not found"
            )
        
        # Get updated reactions
        reactions = ReactionService.get_message_reactions(db, message_id)
        
        # Send real-time update
        reaction_update = {
            "type": "reaction_update",
            "message_id": message_id,
            "reactions": reactions,
            "user_id": user_id,
            "action": "removed",
            "emoji": emoji
        }
        
        await manager.broadcast_json(reaction_update)
        
        return {
            "success": True,
            "reactions": reactions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove reaction: {str(e)}"
        )

@router.get("/message/{message_id}")
async def get_message_reactions(
    message_id: str,
    db: Session = Depends(get_db)
):
    """Get all reactions for a specific message"""
    
    try:
        reactions = ReactionService.get_message_reactions(db, message_id)
        return {
            "message_id": message_id,
            "reactions": reactions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get reactions: {str(e)}"
        )

@router.get("/message/{message_id}/summary")
async def get_reaction_summary(
    message_id: str,
    db: Session = Depends(get_db)
):
    """Get reaction summary for a message"""
    
    try:
        summary = ReactionService.get_message_reaction_summary(db, message_id)
        return summary
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get reaction summary: {str(e)}"
        )

@router.get("/user/{user_id}/reactions")
async def get_user_reactions(
    message_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user's reactions for a specific message"""
    
    try:
        reactions = ReactionService.get_user_reactions_for_message(db, message_id, user_id)
        return {
            "message_id": message_id,
            "user_id": user_id,
            "reactions": reactions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user reactions: {str(e)}"
        )

@router.get("/popular")
async def get_popular_reactions(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get most popular reactions"""
    
    try:
        popular = ReactionService.get_popular_reactions(db, limit)
        return {
            "popular_reactions": popular
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get popular reactions: {str(e)}"
        )

@router.get("/user/{user_id}/history")
async def get_user_reaction_history(
    user_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get user's reaction history"""
    
    try:
        history = ReactionService.get_user_reaction_history(db, user_id, limit)
        return {
            "user_id": user_id,
            "reaction_history": history
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get reaction history: {str(e)}"
        )

@router.post("/bulk")
async def bulk_add_reactions(
    reactions: List[ReactionCreate],
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Add multiple reactions at once"""
    
    try:
        reactions_data = []
        for reaction in reactions:
            reactions_data.append({
                "message_id": reaction.message_id,
                "user_id": user_id,
                "emoji": reaction.emoji,
                "emoji_name": reaction.emoji_name
            })
        
        created_reactions = ReactionService.bulk_add_reactions(db, reactions_data)
        
        return {
            "success": True,
            "created_count": len(created_reactions),
            "reactions": [
                {
                    "id": r.id,
                    "message_id": r.message_id,
                    "emoji": r.emoji,
                    "emoji_name": r.emoji_name
                }
                for r in created_reactions
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to bulk add reactions: {str(e)}"
        )
