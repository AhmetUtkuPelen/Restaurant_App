"""
Message Reaction Service
Handles emoji reactions to messages
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Dict, Optional
from Models.database_models import MessageReactionDB, MessageDB, UserDB
from datetime import datetime
import uuid

class ReactionService:
    
    @staticmethod
    def add_reaction(db: Session, message_id: str, user_id: str, emoji: str, emoji_name: str = None) -> MessageReactionDB:
        """Add a reaction to a message"""
        
        # Check if user already reacted with this emoji
        existing_reaction = db.query(MessageReactionDB).filter(
            and_(
                MessageReactionDB.message_id == message_id,
                MessageReactionDB.user_id == user_id,
                MessageReactionDB.emoji == emoji
            )
        ).first()
        
        if existing_reaction:
            # User already reacted with this emoji, remove it (toggle)
            db.delete(existing_reaction)
            db.commit()
            return None
        
        # Create new reaction
        reaction = MessageReactionDB(
            id=str(uuid.uuid4()),
            message_id=message_id,
            user_id=user_id,
            emoji=emoji,
            emoji_name=emoji_name
        )
        
        db.add(reaction)
        db.commit()
        db.refresh(reaction)
        
        return reaction
    
    @staticmethod
    def remove_reaction(db: Session, message_id: str, user_id: str, emoji: str) -> bool:
        """Remove a specific reaction from a message"""
        
        reaction = db.query(MessageReactionDB).filter(
            and_(
                MessageReactionDB.message_id == message_id,
                MessageReactionDB.user_id == user_id,
                MessageReactionDB.emoji == emoji
            )
        ).first()
        
        if reaction:
            db.delete(reaction)
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def get_message_reactions(db: Session, message_id: str) -> List[Dict]:
        """Get all reactions for a message, grouped by emoji"""
        
        reactions = db.query(MessageReactionDB).filter(
            MessageReactionDB.message_id == message_id
        ).all()
        
        # Group reactions by emoji
        reaction_groups = {}
        for reaction in reactions:
            emoji = reaction.emoji
            if emoji not in reaction_groups:
                reaction_groups[emoji] = {
                    "emoji": emoji,
                    "emoji_name": reaction.emoji_name,
                    "count": 0,
                    "users": [],
                    "user_reacted": False
                }
            
            reaction_groups[emoji]["count"] += 1
            
            # Get user info
            user = db.query(UserDB).filter(UserDB.id == reaction.user_id).first()
            if user:
                reaction_groups[emoji]["users"].append({
                    "id": user.id,
                    "username": user.username,
                    "display_name": user.display_name
                })
        
        return list(reaction_groups.values())
    
    @staticmethod
    def get_user_reactions_for_message(db: Session, message_id: str, user_id: str) -> List[str]:
        """Get all emojis that a user has reacted with for a specific message"""
        
        reactions = db.query(MessageReactionDB).filter(
            and_(
                MessageReactionDB.message_id == message_id,
                MessageReactionDB.user_id == user_id
            )
        ).all()
        
        return [reaction.emoji for reaction in reactions]
    
    @staticmethod
    def get_popular_reactions(db: Session, limit: int = 10) -> List[Dict]:
        """Get most popular reactions across all messages"""
        
        from sqlalchemy import func
        
        popular_reactions = db.query(
            MessageReactionDB.emoji,
            MessageReactionDB.emoji_name,
            func.count(MessageReactionDB.id).label('count')
        ).group_by(
            MessageReactionDB.emoji,
            MessageReactionDB.emoji_name
        ).order_by(
            func.count(MessageReactionDB.id).desc()
        ).limit(limit).all()
        
        return [
            {
                "emoji": reaction.emoji,
                "emoji_name": reaction.emoji_name,
                "count": reaction.count
            }
            for reaction in popular_reactions
        ]
    
    @staticmethod
    def get_message_reaction_summary(db: Session, message_id: str) -> Dict:
        """Get a summary of reactions for a message"""
        
        reactions = ReactionService.get_message_reactions(db, message_id)
        total_reactions = sum(r["count"] for r in reactions)
        unique_users = len(set(
            user["id"] for reaction in reactions for user in reaction["users"]
        ))
        
        return {
            "message_id": message_id,
            "total_reactions": total_reactions,
            "unique_users": unique_users,
            "reaction_types": len(reactions),
            "reactions": reactions
        }
    
    @staticmethod
    def bulk_add_reactions(db: Session, reactions_data: List[Dict]) -> List[MessageReactionDB]:
        """Add multiple reactions at once"""
        
        reactions = []
        for data in reactions_data:
            reaction = MessageReactionDB(
                id=str(uuid.uuid4()),
                message_id=data["message_id"],
                user_id=data["user_id"],
                emoji=data["emoji"],
                emoji_name=data.get("emoji_name")
            )
            reactions.append(reaction)
        
        db.add_all(reactions)
        db.commit()
        
        for reaction in reactions:
            db.refresh(reaction)
        
        return reactions
    
    @staticmethod
    def remove_all_reactions_from_message(db: Session, message_id: str) -> int:
        """Remove all reactions from a message"""
        
        deleted_count = db.query(MessageReactionDB).filter(
            MessageReactionDB.message_id == message_id
        ).delete()
        
        db.commit()
        return deleted_count
    
    @staticmethod
    def get_user_reaction_history(db: Session, user_id: str, limit: int = 50) -> List[Dict]:
        """Get a user's reaction history"""
        
        reactions = db.query(MessageReactionDB).filter(
            MessageReactionDB.user_id == user_id
        ).order_by(
            MessageReactionDB.created_at.desc()
        ).limit(limit).all()
        
        result = []
        for reaction in reactions:
            message = db.query(MessageDB).filter(MessageDB.id == reaction.message_id).first()
            if message:
                result.append({
                    "reaction_id": reaction.id,
                    "emoji": reaction.emoji,
                    "emoji_name": reaction.emoji_name,
                    "created_at": reaction.created_at,
                    "message": {
                        "id": message.id,
                        "content": message.content[:100] + "..." if len(message.content) > 100 else message.content,
                        "sender_id": message.sender_id,
                        "created_at": message.created_at
                    }
                })
        
        return result
