from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Connection manager to handle WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.users: dict = {}  # websocket -> username mapping

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.users[websocket] = username
        
        # Notify others that user joined
        await self.broadcast_message({
            "type": "user_joined",
            "username": username,
            "message": f"{username} joined the chat"
        }, exclude=websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            username = self.users.get(websocket, "Unknown")
            self.active_connections.remove(websocket)
            del self.users[websocket]
            return username
        return None

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, message: dict, exclude: WebSocket = None):
        message_str = json.dumps(message)
        for connection in self.active_connections:
            if connection != exclude:
                try:
                    await connection.send_text(message_str)
                except:
                    # Remove broken connections
                    self.active_connections.remove(connection)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Chat API is running"}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Broadcast message to all connected clients
            await manager.broadcast_message({
                "type": "message",
                "username": username,
                "message": message_data.get("message", ""),
                "timestamp": message_data.get("timestamp")
            })
            
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast_message({
                "type": "user_left",
                "username": username,
                "message": f"{username} left the chat"
            })