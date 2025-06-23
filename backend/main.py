from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
# Import routers from respective files
from Routes.User.UserRoutes import router as user_router
from Routes.Message.MessageRoutes import router as message_router
from Routes.FileUpload.FileUploadRoutes import router as file_router
from Routes.Reactions.ReactionRoutes import router as reaction_router
from Routes.Rooms.RoomRoutes import router as room_router
from Routes.Search.SearchRoutes import router as search_router
from Routes.Notifications.NotificationRoutes import router as notification_router
from Routes.Calls.CallRoutes import router as call_router

# Import database from database.py
from database import create_tables

# Import WebSocket manager
from Services.WebSocketManager import manager

# Add CORS middleware for front end communication
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI(title="Chat API", version="1.0.0")


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


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat"""
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

# backend landing page for testing
@app.get("/")
async def get():
    return {"message": "Chat API is running"}

# Endpoint to seed admin user
@app.post("/seed-admin")
async def seed_admin():
    """Endpoint to seed admin user - for development only"""
    try:
        from seed_admin import seed_admin_user
        seed_admin_user()
        return {"message": "Admin user seeded successfully", "username": "admin", "password": "admin123"}
    except Exception as e:
        return {"error": f"Failed to seed admin user: {str(e)}"}




# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173" , "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
