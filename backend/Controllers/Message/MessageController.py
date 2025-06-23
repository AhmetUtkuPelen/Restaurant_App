from sqlalchemy.orm import Session
from typing import List
from Services.MessageService import MessageService
from Schemas.Message.MessageSchemas import MessageCreate, MessageUpdate, MessageResponse

class MessageController:
    def __init__(self):
        pass

    async def create_message(self, db: Session, sender_id: str, message_data: MessageCreate) -> MessageResponse:
        """Create a new message"""
        return await self.message_service.create_message(db, sender_id, message_data)

    async def get_message_by_id(self, db: Session, message_id: str) -> MessageResponse:
        """Get message by ID"""
        return await self.message_service.get_message_by_id(db, message_id)

    async def update_message(self, db: Session, message_id: str, sender_id: str, update_data: MessageUpdate) -> MessageResponse:
        """Update a message (only sender can edit)"""
        return await self.message_service.update_message(db, message_id, sender_id, update_data)

    async def delete_message(self, db: Session, message_id: str, user_id: str) -> dict:
        """Delete a message (only sender can delete)"""
        return await self.message_service.delete_message(db, message_id, user_id)

    async def get_conversation_messages(
        self,
        db: Session,
        user1_id: str,
        user2_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[MessageResponse]:
        """Get messages between two users"""
        return await self.message_service.get_conversation_messages(db, user1_id, user2_id, skip, limit)

    async def get_chat_messages(
        self,
        db: Session,
        chat_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[MessageResponse]:
        """Get messages for a specific chat/group"""
        return await self.message_service.get_chat_messages(db, chat_id, skip, limit)

    async def add_reaction(self, db: Session, message_id: str, user_id: str, emoji: str) -> MessageResponse:
        """Add a reaction to a message"""
        return await self.message_service.add_reaction(db, message_id, user_id, emoji)

    async def remove_reaction(self, db: Session, message_id: str, user_id: str, emoji: str) -> MessageResponse:
        """Remove a reaction from a message"""
        return await self.message_service.remove_reaction(db, message_id, user_id, emoji)

    async def mark_message_as_read(self, db: Session, message_id: str, user_id: str) -> MessageResponse:
        """Mark a message as read"""
        return await self.message_service.mark_message_as_read(db, message_id, user_id)


