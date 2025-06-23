from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import json

# Import routers
from backend.Routes.User.UserRoutes import router as user_router
from backend.Routes.Message.MessageRoutes import router as message_router

# Import database
from backend.database import create_tables

app = FastAPI(title="Real-time Chat API", version="1.0.0")

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Include routers
app.include_router(user_router)
app.include_router(message_router)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: dict = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections.remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender_id: str = None):
        for connection in self.active_connections:
            if sender_id and self.user_connections.get(sender_id) == connection:
                continue  # Don't send back to sender
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Broadcast message to all connected clients
            broadcast_message = {
                "user_id": user_id,
                "message": message_data.get("message"),
                "timestamp": message_data.get("timestamp")
            }
            await manager.broadcast(json.dumps(broadcast_message))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        # Notify others that user left
        leave_message = {
            "user_id": "system",
            "message": f"{user_id} left the chat",
            "timestamp": ""
        }
        await manager.broadcast(json.dumps(leave_message))

@app.get("/")
async def get():
    return {"message": "Chat API is running"}

# Optional: Add CORS middleware if needed
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
