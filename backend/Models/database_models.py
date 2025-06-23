from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from Models.User.UserModel import UserStatus, UserRole
from Models.Message.MessageModel import MessageType, MessageStatus, AttachmentType
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    avatar_url = Column(String(500))
    bio = Column(String(500))
    status = Column(SQLEnum(UserStatus), default=UserStatus.OFFLINE)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_seen = Column(DateTime(timezone=True))
    friends = Column(JSON, default=list)  # List of user IDs
    blocked_users = Column(JSON, default=list)  # List of blocked user IDs
    
    # Relationships
    sent_messages = relationship("MessageDB", foreign_keys="MessageDB.sender_id", back_populates="sender")
    received_messages = relationship("MessageDB", foreign_keys="MessageDB.recipient_id", back_populates="recipient")
    reactions = relationship("MessageReactionDB", back_populates="user")

class AttachmentDB(Base):
    __tablename__ = "attachments"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    attachment_type = Column(SQLEnum(AttachmentType), nullable=False)
    url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Integer)  # For audio/video in seconds
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    
    # Relationships
    message = relationship("MessageDB", back_populates="attachments")

class MessageReactionDB(Base):
    __tablename__ = "message_reactions"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    emoji = Column(String(10), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("UserDB", back_populates="reactions")
    message = relationship("MessageDB", back_populates="reactions")

class MessageDB(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    sender_id = Column(String, ForeignKey("users.id"), nullable=False)
    chat_id = Column(String, index=True)  # For group chats
    recipient_id = Column(String, ForeignKey("users.id"))  # For direct messages
    content = Column(Text)
    message_type = Column(SQLEnum(MessageType), default=MessageType.TEXT)
    reply_to_message_id = Column(String, ForeignKey("messages.id"))
    status = Column(SQLEnum(MessageStatus), default=MessageStatus.SENT)
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    delivered_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    message_metadata = Column(JSON, default=dict)  # For additional data
    
    # Relationships
    sender = relationship("UserDB", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("UserDB", foreign_keys=[recipient_id], back_populates="received_messages")
    attachments = relationship("AttachmentDB", back_populates="message", cascade="all, delete-orphan")
    reactions = relationship("MessageReactionDB", back_populates="message", cascade="all, delete-orphan")
    
    # Self-referential relationship for replies
    reply_to = relationship("MessageDB", remote_side=[id])

class ChatRoomDB(Base):
    __tablename__ = "chat_rooms"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    is_private = Column(Boolean, default=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    members = Column(JSON, default=list)  # List of user IDs
    admins = Column(JSON, default=list)  # List of admin user IDs
    
    # Relationships
    creator = relationship("UserDB")

class ChatMemberDB(Base):
    __tablename__ = "chat_members"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    chat_id = Column(String, ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_admin = Column(Boolean, default=False)
    is_muted = Column(Boolean, default=False)
    
    # Relationships
    chat = relationship("ChatRoomDB")
    user = relationship("UserDB")
