from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
import logging

# Import configuration
from config import settings

# Import routers from respective files
from Routes.User.UserRoutes import router as user_router
from Routes.Message.MessageRoutes import router as message_router
from Routes.FileUpload.FileUploadRoutes import router as file_router
from Routes.Reactions.ReactionRoutes import router as reaction_router
from Routes.Rooms.RoomRoutes import router as room_router
from Routes.Search.SearchRoutes import router as search_router
from Routes.Notifications.NotificationRoutes import router as notification_router
from Routes.Calls.CallRoutes import router as call_router
from Routes.Admin.AdminRoutes import router as admin_router

# Import database from database.py
from database import create_tables

# Import WebSocket manager
from Services.WebSocketManager import manager
from Services.OpenAPIService import OpenAPIService

# Import middleware
from fastapi.middleware.cors import CORSMiddleware
from Services.ErrorHandlingService import ErrorHandlerMiddleware
from middleware.rate_limit import RateLimitMiddleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI instance with comprehensive OpenAPI configuration
app = FastAPI(
    title="Real-time Chat API",
    version="1.0.0",
    description="""
    ## Real-time Chat Application API

    A secure, scalable real-time chat application with comprehensive features including:

    * **User Management**: Registration, authentication, profile management
    * **Real-time Messaging**: WebSocket-based instant messaging
    * **File Uploads**: Secure file sharing with validation
    * **Chat Rooms**: Group conversations and private messaging
    * **Reactions**: Message reactions and emoji support
    * **Search**: Message and user search functionality
    * **Admin Panel**: Administrative controls and monitoring
    * **Security**: JWT authentication, rate limiting, input validation

    ### Authentication

    This API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

    1. Register a new account or login with existing credentials
    2. Use the returned JWT token in the Authorization header
    3. Format: `Authorization: Bearer <your-jwt-token>`

    ### Rate Limiting

    API requests are rate-limited to prevent abuse:
    - Default: 100 requests per hour per user
    - Failed login attempts trigger account lockout
    - File uploads have separate size and type restrictions

    ### WebSocket Connection

    Real-time features use WebSocket connections at `/ws/{user_id}`.
    Authentication is required for WebSocket connections.
    """,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Chat API Support",
        "email": "support@chatapi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.chatapp.com",
            "description": "Production server"
        }
    ],
    tags_metadata=[
        {
            "name": "users",
            "description": "User management operations including registration, authentication, and profile management.",
        },
        {
            "name": "messages",
            "description": "Message operations for sending, receiving, and managing chat messages.",
        },
        {
            "name": "files",
            "description": "File upload and management operations with security validation.",
        },
        {
            "name": "reactions",
            "description": "Message reaction operations for emoji responses.",
        },
        {
            "name": "rooms",
            "description": "Chat room management for group conversations.",
        },
        {
            "name": "search",
            "description": "Search operations for messages and users.",
        },
        {
            "name": "notifications",
            "description": "Notification management and delivery.",
        },
        {
            "name": "calls",
            "description": "Voice and video call management.",
        },
        {
            "name": "admin",
            "description": "Administrative operations for system management and monitoring.",
        },
        {
            "name": "websocket",
            "description": "Real-time WebSocket connections for instant messaging.",
        },
    ]
)

# Add error handling middleware FIRST
app.add_middleware(ErrorHandlerMiddleware)

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    default_requests=settings.rate_limit_requests,
    default_window=settings.rate_limit_window
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Import Routers
app.include_router(user_router)
app.include_router(message_router)
app.include_router(file_router)
app.include_router(reaction_router)
app.include_router(room_router)
app.include_router(search_router)
app.include_router(notification_router)
app.include_router(call_router)
app.include_router(admin_router)

# Custom OpenAPI schema
@app.get("/openapi.json", include_in_schema=False)
async def custom_openapi():
    """Custom OpenAPI schema with enhanced documentation."""
    return OpenAPIService.get_custom_openapi(app)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time chat communication.
    
    **Connection Process:**
    1. Connect to `/ws/{user_id}` with valid user ID
    2. Authentication is handled via query parameters or headers
    3. Connection is maintained for real-time message exchange
    
    **Message Format:**
    ```json
    {
        "message": "Hello, world!",
        "timestamp": "2024-01-01T12:00:00Z",
        "attachments": []
    }
    ```
    
    **Response Format:**
    ```json
    {
        "id": "msg_1234567890",
        "sender_id": "user123",
        "content": "Hello, world!",
        "created_at": "2024-01-01T12:00:00Z",
        "status": "delivered"
    }
    ```
    
    **Connection Events:**
    - User connects: Broadcasts user online status
    - Message sent: Broadcasts to all connected users
    - User disconnects: Broadcasts user offline status
    
    **Error Handling:**
    - Invalid user ID: Connection rejected
    - Authentication failure: Connection closed
    - Network issues: Automatic reconnection attempted
    """
    # Extract user info from query parameters or use defaults
    user_info = {
        "id": user_id,
        "username": user_id,
        "display_name": user_id,
        "connected_at": datetime.utcnow().isoformat()
    }

    await manager.connect(websocket, user_id, user_info)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Create message object
            message = {
                "id": f"msg_{datetime.utcnow().timestamp()}",
                "sender_id": user_id,
                "content": message_data.get("message", ""),
                "created_at": message_data.get("timestamp", datetime.utcnow().isoformat()),
                "attachments": message_data.get("attachments", []),
                "is_edited": False,
                "status": "sent"
            }

            # Broadcast message to all connected users
            await manager.broadcast_json(message, exclude_user=user_id)

            # Send confirmation back to sender
            confirmation = {
                **message,
                "status": "delivered"
            }
            await manager.send_personal_json(confirmation, user_id)

    except WebSocketDisconnect:
        await manager.disconnect(user_id)
    except Exception as e:
        # Log any other unexpected errors
        print(f"WebSocket error for user {user_id}: {e}")
        await manager.disconnect(user_id)

# backend landing page for testing
@app.get(
    "/",
    tags=["health"],
    summary="API Health Check",
    description="Simple health check endpoint to verify the API is running.",
    responses={
        200: {
            "description": "API is running successfully",
            "content": {
                "application/json": {
                    "example": {"message": "Chat API is running"}
                }
            }
        }
    }
)
async def get():
    """
    Health check endpoint for the Chat API.
    
    Returns a simple message confirming the API is operational.
    This endpoint can be used by load balancers and monitoring systems.
    """
    return {"message": "Chat API is running"}

# Test endpoint for debugging
@app.get(
    "/test-db",
    tags=["health"],
    summary="Database Connection Test",
    description="Test database connectivity and return basic statistics.",
    responses={
        200: {
            "description": "Database connection successful",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Database connection successful",
                        "user_count": 42
                    }
                }
            }
        },
        500: {
            "description": "Database connection failed",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Database error: Connection refused"
                    }
                }
            }
        }
    }
)
async def test_db():
    """
    Test database connectivity and return basic statistics.
    
    This endpoint verifies that the database connection is working
    and returns the total number of users as a simple health check.
    
    **Use Cases:**
    - Health monitoring
    - Database connectivity verification
    - Basic system diagnostics
    """
    try:
        from database import get_db
        from Models.database_models import UserDB
        from sqlalchemy.orm import Session

        # Get a database session
        db_gen = get_db()
        db = next(db_gen)

        # Try to query users
        users = db.query(UserDB).all()
        return {"message": "Database connection successful", "user_count": len(users)}
    except Exception as e:
        return {"error": f"Database error: {str(e)}"}

# Endpoint to seed admin user
@app.post(
    "/seed-admin",
    tags=["development"],
    summary="Seed Admin User",
    description="Create default admin user for development purposes. **WARNING: Development only!**",
    responses={
        200: {
            "description": "Admin user created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Admin user seeded successfully",
                        "username": "admin",
                        "password": "admin123"
                    }
                }
            }
        },
        500: {
            "description": "Failed to create admin user",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Failed to seed admin user: User already exists"
                    }
                }
            }
        }
    }
)
async def seed_admin():
    """
    Create a default admin user for development purposes.
    
    **⚠️ WARNING: This endpoint should only be used in development!**
    
    Creates an admin user with default credentials:
    - Username: admin
    - Password: admin123
    
    **Security Notes:**
    - This endpoint should be disabled in production
    - Default credentials should be changed immediately
    - Only use for initial setup and testing
    """
    try:
        from seed_admin import seed_admin_user
        seed_admin_user()
        return {"message": "Admin user seeded successfully", "username": "admin", "password": "admin123"}
    except Exception as e:
        return {"error": f"Failed to seed admin user: {str(e)}"}





