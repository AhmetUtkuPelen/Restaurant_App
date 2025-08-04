from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, JSON, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from Models.User.UserModel import UserStatus, UserRole
from Models.Message.MessageModel import MessageType, MessageStatus, AttachmentType
from Services.SoftDeleteService import SoftDeleteMixin
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class UserDB(Base, SoftDeleteMixin):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Security fields
    salt = Column(String(255), nullable=True)  # Will be populated and made non-nullable later
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    last_password_change = Column(DateTime(timezone=True), server_default=func.now())
    
    # Profile fields
    display_name = Column(String(100))
    avatar_url = Column(String(500))
    bio = Column(String(500))
    status = Column(SQLEnum(UserStatus), default=UserStatus.OFFLINE)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    
    # Account status fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)  # Soft delete flag
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete timestamp
    
    # User preferences and settings
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    friends = Column(JSON, default=list)  # List of user IDs
    blocked_users = Column(JSON, default=list)  # List of blocked user IDs
    
    # Relationships
    sent_messages = relationship("MessageDB", foreign_keys="MessageDB.sender_id", back_populates="sender")
    received_messages = relationship("MessageDB", foreign_keys="MessageDB.recipient_id", back_populates="recipient")
    reactions = relationship("MessageReactionDB", back_populates="user")
    audit_logs = relationship("AuditLogDB", back_populates="user")
    
    # Indexes for performance optimization
    __table_args__ = (
        Index('idx_users_email_active', 'email', 'is_active'),
        Index('idx_users_username_active', 'username', 'is_active'),
        Index('idx_users_status_last_seen', 'status', 'last_seen'),
        Index('idx_users_role_active', 'role', 'is_active'),
        Index('idx_users_created_at', 'created_at'),
        Index('idx_users_failed_attempts', 'failed_login_attempts'),
        Index('idx_users_locked_until', 'locked_until'),
    )

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
    emoji_name = Column(String, nullable=True)  # Emoji name (e.g., "thumbs_up")
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("UserDB", back_populates="reactions")
    message = relationship("MessageDB", back_populates="reactions")

class MessageDB(Base, SoftDeleteMixin):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    sender_id = Column(String, ForeignKey("users.id"), nullable=False)
    chat_id = Column(String, ForeignKey("chat_rooms.id"), index=True)  # For group chats
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
    room = relationship("ChatRoomDB", foreign_keys=[chat_id])
    attachments = relationship("AttachmentDB", back_populates="message", cascade="all, delete-orphan")
    reactions = relationship("MessageReactionDB", back_populates="message", cascade="all, delete-orphan")

    # Self-referential relationship for replies
    reply_to = relationship("MessageDB", remote_side=[id])
    
    # Indexes for performance optimization
    __table_args__ = (
        Index('idx_messages_sender_created', 'sender_id', 'created_at'),
        Index('idx_messages_recipient_created', 'recipient_id', 'created_at'),
        Index('idx_messages_chat_created', 'chat_id', 'created_at'),
        Index('idx_messages_type_created', 'message_type', 'created_at'),
        Index('idx_messages_status', 'status'),
        Index('idx_messages_deleted', 'is_deleted'),
    )

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



class NotificationDB(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, nullable=False)  # message, mention, room_invite, etc.
    data = Column(JSON, default=dict)  # Additional notification data
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("UserDB")

class CallSessionDB(Base):
    __tablename__ = "call_sessions"

    id = Column(String, primary_key=True, default=generate_uuid)
    room_id = Column(String, ForeignKey("chat_rooms.id"), nullable=True)
    caller_id = Column(String, ForeignKey("users.id"), nullable=False)
    call_type = Column(String, nullable=False)  # audio, video
    status = Column(String, default="initiated")  # initiated, ringing, active, ended
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, default=0)  # in seconds

    # Relationships
    caller = relationship("UserDB", foreign_keys=[caller_id])
    room = relationship("ChatRoomDB")
    participants = relationship("CallParticipantDB", back_populates="call")

class CallParticipantDB(Base):
    __tablename__ = "call_participants"

    id = Column(String, primary_key=True, default=generate_uuid)
    call_id = Column(String, ForeignKey("call_sessions.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="invited")  # invited, joined, left, rejected

    # Relationships
    call = relationship("CallSessionDB", back_populates="participants")
    user = relationship("UserDB")
class AuditLogDB(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(String, nullable=True, index=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    session_id = Column(String, nullable=True)
    request_id = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Additional security tracking
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    risk_level = Column(String(20), default="low")  # low, medium, high, critical
    
    # Relationships
    user = relationship("UserDB", back_populates="audit_logs")
    
    @classmethod
    def create_log(cls, db, user_id=None, action=None, resource_type=None, resource_id=None, 
                   details=None, ip_address=None, user_agent=None, session_id=None, 
                   request_id=None, success=True, error_message=None, risk_level="low"):
        """
        Create a new audit log entry.
        
        Args:
            db: Database session
            user_id: ID of the user performing the action
            action: Action being performed
            resource_type: Type of resource being acted upon
            resource_id: ID of the specific resource
            details: Additional details as JSON
            ip_address: IP address of the request
            user_agent: User agent string
            session_id: Session ID
            request_id: Request ID for tracing
            success: Whether the action was successful
            error_message: Error message if action failed
            risk_level: Risk level (low, medium, high, critical)
            
        Returns:
            AuditLogDB: The created audit log entry
        """
        audit_log = cls(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            request_id=request_id,
            success=success,
            error_message=error_message,
            risk_level=risk_level
        )
        db.add(audit_log)
        db.commit()
        return audit_log
    
    @classmethod
    def get_user_activity(cls, db, user_id, limit=50):
        """Get recent activity for a specific user."""
        return db.query(cls).filter(cls.user_id == user_id).order_by(cls.timestamp.desc()).limit(limit).all()
    
    @classmethod
    def get_failed_attempts(cls, db, user_id=None, ip_address=None, hours=24):
        """Get failed login attempts for a user or IP address within specified hours."""
        from datetime import datetime, timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = db.query(cls).filter(
            cls.action == "login",
            cls.success == False,
            cls.timestamp >= cutoff_time
        )
        
        if user_id:
            query = query.filter(cls.user_id == user_id)
        if ip_address:
            query = query.filter(cls.ip_address == ip_address)
            
        return query.all()
    
    @classmethod
    def get_high_risk_activities(cls, db, hours=24):
        """Get high-risk activities within specified hours."""
        from datetime import datetime, timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        return db.query(cls).filter(
            cls.risk_level.in_(["high", "critical"]),
            cls.timestamp >= cutoff_time
        ).order_by(cls.timestamp.desc()).all()

class AppConfigDB(Base):
    __tablename__ = "app_config"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    is_sensitive = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())