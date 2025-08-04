from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status
from typing import List, Optional
from Models.database_models import MessageDB, MessageReactionDB, UserDB
from Models.Message.MessageModel import MessageStatus
from Schemas.Message.MessageSchemas import MessageCreate, MessageUpdate, MessageResponse
from datetime import datetime
from Services.ReactionService import ReactionService

class MessageService:
    def __init__(self):
        self.reaction_service = ReactionService()
    
    async def _message_to_response(self, message: MessageDB) -> MessageResponse:
        """Convert MessageDB to MessageResponse"""
        return MessageResponse(
            id=message.id,
            sender_id=message.sender_id,
            chat_id=message.chat_id,
            recipient_id=message.recipient_id,
            content=message.content,
            message_type=message.message_type,
            attachments=[],  # TODO: Convert attachments
            reply_to_message_id=message.reply_to_message_id,
            reactions=[],  # TODO: Convert reactions
            status=message.status,
            is_edited=message.is_edited,
            is_deleted=message.is_deleted,
            created_at=message.created_at,
            updated_at=message.updated_at,
            delivered_at=message.delivered_at,
            read_at=message.read_at
        )
    
    async def create_message(self, db: Session, sender_id: str, message_data: MessageCreate) -> MessageResponse:
        """Create a new message"""
        # Validate that either recipient_id or chat_id is provided
        if not message_data.recipient_id and not message_data.chat_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either recipient_id or chat_id must be provided"
            )
        
        # Verify sender exists
        sender = db.query(UserDB).filter(UserDB.id == sender_id).first()
        if not sender:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sender not found"
            )
        
        # Verify recipient exists (if direct message)
        if message_data.recipient_id:
            recipient = db.query(UserDB).filter(UserDB.id == message_data.recipient_id).first()
            if not recipient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Recipient not found"
                )
        
        # Create new message
        db_message = MessageDB(
            sender_id=sender_id,
            recipient_id=message_data.recipient_id,
            chat_id=message_data.chat_id,
            content=message_data.content,
            message_type=message_data.message_type,
            reply_to_message_id=message_data.reply_to_message_id,
            message_metadata=message_data.metadata
        )
        
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        return await self._message_to_response(db_message)
    
    async def get_message_by_id(self, db: Session, message_id: str) -> MessageResponse:
        """Get message by ID"""
        message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        return await self._message_to_response(message)
    
    async def update_message(self, db: Session, message_id: str, sender_id: str, update_data: MessageUpdate) -> MessageResponse:
        """Update a message (only sender can edit)"""
        message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Check if user is the sender
        if message.sender_id != sender_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own messages"
            )
        
        # Update message
        if update_data.content is not None:
            message.content = update_data.content
        message.is_edited = True
        message.updated_at = datetime.utcnow()
        
        db.commit()
        
        return await self._message_to_response(message)
    
    async def delete_message(self, db: Session, message_id: str, user_id: str) -> dict:
        """Delete a message (only sender can delete)"""
        message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Check if user is the sender
        if message.sender_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own messages"
            )
        
        # Mark as deleted instead of actually deleting
        message.is_deleted = True
        message.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Message deleted successfully"}
    
    async def get_conversation_messages(
        self, 
        db: Session,
        user1_id: str, 
        user2_id: str, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[MessageResponse]:
        """Get messages between two users"""
        messages = db.query(MessageDB).filter(
            and_(
                MessageDB.is_deleted == False,
                or_(
                    and_(MessageDB.sender_id == user1_id, MessageDB.recipient_id == user2_id),
                    and_(MessageDB.sender_id == user2_id, MessageDB.recipient_id == user1_id)
                )
            )
        ).order_by(MessageDB.created_at.desc()).offset(skip).limit(limit).all()
        
        return [await self._message_to_response(msg) for msg in messages]
    
    async def get_chat_messages(
        self, 
        db: Session,
        chat_id: str, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[MessageResponse]:
        """Get messages for a specific chat/group"""
        messages = db.query(MessageDB).filter(
            and_(
                MessageDB.chat_id == chat_id,
                MessageDB.is_deleted == False
            )
        ).order_by(MessageDB.created_at.desc()).offset(skip).limit(limit).all()
        
        return [await self._message_to_response(msg) for msg in messages]
    
    async def add_reaction(self, db: Session, message_id: str, user_id: str, emoji: str) -> MessageResponse:
        """Add a reaction to a message"""
        message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Check if user already reacted with this emoji
        existing_reaction = db.query(MessageReactionDB).filter(
            and_(
                MessageReactionDB.message_id == message_id,
                MessageReactionDB.user_id == user_id,
                MessageReactionDB.emoji == emoji
            )
        ).first()
        
        if existing_reaction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already reacted with this emoji"
            )
        
        # Add reaction
        new_reaction = MessageReactionDB(
            emoji=emoji,
            user_id=user_id,
            message_id=message_id
        )
        
        db.add(new_reaction)
        db.commit()
        
        return await self._message_to_response(message)
    
    async def remove_reaction(self, db: Session, message_id: str, user_id: str, emoji: str) -> MessageResponse:
        """Remove a reaction from a message"""
        message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Find and remove the reaction
        reaction = db.query(MessageReactionDB).filter(
            and_(
                MessageReactionDB.message_id == message_id,
                MessageReactionDB.user_id == user_id,
                MessageReactionDB.emoji == emoji
            )
        ).first()
        
        if not reaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reaction not found"
            )
        
        db.delete(reaction)
        db.commit()
        
        return await self._message_to_response(message)
    
    async def mark_message_as_read(self, db: Session, message_id: str, user_id: str) -> MessageResponse:
        """Mark a message as read"""
        message = db.query(MessageDB).filter(MessageDB.id == message_id).first()
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Only recipient can mark as read
        if message.recipient_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only mark messages sent to you as read"
            )
        
        message.status = MessageStatus.READ
        message.read_at = datetime.utcnow()
        db.commit()

        return await self._message_to_response(message)

    async def get_user_messages(
        self,
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[MessageResponse]:
        """Get all messages for a user (recent conversations)"""
        # Get messages where user is either sender or recipient
        messages = db.query(MessageDB).filter(
            or_(
                MessageDB.sender_id == user_id,
                MessageDB.recipient_id == user_id
            ),
            MessageDB.is_deleted == False
        ).order_by(MessageDB.created_at.desc()).offset(skip).limit(limit).all()

        return [await self._message_to_response(message) for message in messages]
