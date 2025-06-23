from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
from Models.Message.MessageModel import MessageType, Attachment, MessageReaction, MessageStatus



class MessageCreate(BaseModel):
    recipient_id: Optional[str] = None
    chat_id: Optional[str] = None
    content: Optional[str] = Field(None, max_length=4000)
    message_type: MessageType = MessageType.TEXT
    reply_to_message_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MessageUpdate(BaseModel):
    content: Optional[str] = Field(None, max_length=4000)
    is_edited: bool = True
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MessageResponse(BaseModel):
    id: str
    sender_id: str
    chat_id: Optional[str]
    recipient_id: Optional[str]
    content: Optional[str]
    message_type: MessageType
    attachments: List[Attachment]
    reply_to_message_id: Optional[str]
    reactions: List[MessageReaction]
    status: MessageStatus
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    delivered_at: Optional[datetime]
    read_at: Optional[datetime]

class MessageWithSender(MessageResponse):
    sender: Dict[str, Any]  # Will contain sender user info

class ReactionCreate(BaseModel):
    emoji: str
    message_id: str

class ReactionResponse(BaseModel):
    emoji: str
    count: int
    users: List[str]  # List of user IDs who reacted
