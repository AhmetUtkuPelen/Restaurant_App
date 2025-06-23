from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"
    EMOJI = "emoji"

class MessageStatus(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

class AttachmentType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"

class Attachment(BaseModel):
    id: str
    filename: str
    original_filename: str
    file_size: int  # in bytes
    mime_type: str
    attachment_type: AttachmentType
    url: str
    thumbnail_url: Optional[str] = None  # For images/videos
    width: Optional[int] = None  # For images
    height: Optional[int] = None  # For images
    duration: Optional[int] = None  # For audio/video in seconds
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class MessageReaction(BaseModel):
    emoji: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(BaseModel):
    id: Optional[str] = None
    sender_id: str
    chat_id: Optional[str] = None  # For group chats
    recipient_id: Optional[str] = None  # For direct messages
    content: Optional[str] = Field(None, max_length=4000)
    message_type: MessageType = MessageType.TEXT
    attachments: List[Attachment] = Field(default_factory=list)
    reply_to_message_id: Optional[str] = None  # For replies
    reactions: List[MessageReaction] = Field(default_factory=list)
    status: MessageStatus = MessageStatus.SENT
    is_edited: bool = False
    is_deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)  # For additional data

    @validator('content')
    def validate_content(cls, v, values):
        message_type = values.get('message_type')
        if message_type == MessageType.TEXT and (not v or len(v.strip()) == 0):
            raise ValueError('Text messages must have content')
        return v

    @validator('attachments')
    def validate_attachments(cls, v, values):
        message_type = values.get('message_type')
        if message_type in [MessageType.IMAGE, MessageType.FILE] and len(v) == 0:
            raise ValueError('Image and file messages must have attachments')
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }