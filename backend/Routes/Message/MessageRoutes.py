from fastapi import APIRouter, status, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from sqlalchemy.orm import Session
from Controllers.Message.MessageController import MessageController
from Schemas.Message.MessageSchemas import (
    MessageCreate, MessageUpdate, MessageResponse
)
from database import get_db
from Services.AuthService import AuthService

# Create router
router = APIRouter(prefix="/messages", tags=["messages"])

# Initialize controller
message_controller = MessageController()

# Security scheme
security = HTTPBearer()

# Dependency to get current user from JWT token
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> str:
    """Get current user ID from JWT token"""
    try:
        token = credentials.credentials
        user_id = AuthService.get_user_id_from_token(token)
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get(
    "/",
    response_model=List[MessageResponse],
    summary="Get Messages",
    description="Retrieve messages from chat rooms, conversations, or user's recent messages.",
    responses={
        200: {
            "description": "Messages retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "msg_123",
                            "sender_id": "user_456",
                            "chat_id": "room_789",
                            "recipient_id": None,
                            "content": "Hello everyone!",
                            "message_type": "text",
                            "attachments": [],
                            "reply_to_message_id": None,
                            "reactions": [
                                {
                                    "emoji": "👍",
                                    "count": 3,
                                    "users": ["user_123", "user_456", "user_789"]
                                }
                            ],
                            "status": "delivered",
                            "is_edited": False,
                            "is_deleted": False,
                            "created_at": "2024-01-01T12:00:00Z",
                            "updated_at": "2024-01-01T12:00:00Z",
                            "delivered_at": "2024-01-01T12:00:01Z",
                            "read_at": "2024-01-01T12:00:05Z"
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Authentication required"
        },
        403: {
            "description": "Access denied to chat room or conversation"
        }
    }
)
async def get_messages(
    chat_id: Optional[str] = Query(None, description="Chat room ID to get messages from"),
    recipient_id: Optional[str] = Query(None, description="User ID for private conversation"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of messages to return"),
    skip: int = Query(0, ge=0, description="Number of messages to skip (for pagination)"),
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Retrieve messages based on different criteria.
    
    **Query Options:**
    1. **Chat Room Messages**: Provide `chat_id` to get messages from a specific room
    2. **Private Conversation**: Provide `recipient_id` to get conversation with a user
    3. **Recent Messages**: No parameters to get user's recent conversations
    
    **Pagination:**
    - Use `skip` and `limit` parameters for pagination
    - Maximum limit is 100 messages per request
    - Messages are returned in reverse chronological order (newest first)
    
    **Message Types:**
    - Text messages
    - File attachments
    - System messages
    - Reply messages
    
    **Security:**
    - Users can only access messages they're authorized to see
    - Private conversations require participation
    - Chat room access is validated
    """
    if chat_id:
        # Get messages from a specific chat room
        return await message_controller.get_chat_messages(db, chat_id, skip, limit)
    elif recipient_id:
        # Get conversation messages between current user and recipient
        return await message_controller.get_conversation_messages(
            db, current_user_id, recipient_id, skip, limit
        )
    else:
        # Get all messages for the current user (recent conversations)
        return await message_controller.get_user_messages(db, current_user_id, skip, limit)

@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send Message",
    description="Send a new message to a chat room or user.",
    responses={
        201: {
            "description": "Message sent successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "msg_123",
                        "sender_id": "user_456",
                        "chat_id": "room_789",
                        "recipient_id": None,
                        "content": "Hello everyone!",
                        "message_type": "text",
                        "attachments": [],
                        "reply_to_message_id": None,
                        "reactions": [],
                        "status": "sent",
                        "is_edited": False,
                        "is_deleted": False,
                        "created_at": "2024-01-01T12:00:00Z",
                        "updated_at": "2024-01-01T12:00:00Z",
                        "delivered_at": None,
                        "read_at": None
                    }
                }
            }
        },
        400: {
            "description": "Invalid message data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Message content cannot be empty"
                    }
                }
            }
        },
        401: {
            "description": "Authentication required"
        },
        403: {
            "description": "Access denied to chat room or user"
        }
    }
)
async def create_message(
    message_data: MessageCreate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Send a new message to a chat room or user.
    
    **Message Types:**
    - **Text**: Regular text message (default)
    - **File**: Message with file attachment
    - **System**: System-generated message
    - **Reply**: Reply to another message
    
    **Destination Options:**
    - **Chat Room**: Set `chat_id` for group messages
    - **Private Message**: Set `recipient_id` for direct messages
    - Cannot set both `chat_id` and `recipient_id`
    
    **Content Validation:**
    - Maximum 4000 characters for text content
    - HTML content is sanitized to prevent XSS
    - File attachments are validated for type and size
    
    **Real-time Delivery:**
    - Messages are immediately broadcast via WebSocket
    - Delivery and read receipts are tracked
    - Offline users receive messages when they reconnect
    
    **Reply Feature:**
    - Set `reply_to_message_id` to reply to a specific message
    - Original message context is preserved
    - Reply chains are supported
    """
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