"""
WebSocket Manager for real-time chat functionality
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store active connections: {user_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Store user information: {user_id: user_info}
        self.connected_users: Dict[str, dict] = {}
        # Store room memberships: {room_id: set of user_ids}
        self.room_members: Dict[str, Set[str]] = {}
        # Store user's current room: {user_id: room_id}
        self.user_rooms: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, user_id: str, user_info: dict = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        
        # Store connection
        self.active_connections[user_id] = websocket
        
        # Store user info
        if user_info:
            self.connected_users[user_id] = user_info
        else:
            self.connected_users[user_id] = {
                "id": user_id,
                "username": user_id,
                "display_name": user_id,
                "connected_at": datetime.utcnow().isoformat()
            }
        
        logger.info(f"User {user_id} connected to WebSocket")
        
        # Notify other users about new connection
        await self.broadcast_user_joined(user_id)
        
        # Send current online users to the new user
        await self.send_online_users(user_id)

    async def disconnect(self, user_id: str):
        """Remove a WebSocket connection"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        if user_id in self.connected_users:
            del self.connected_users[user_id]
        
        # Remove from any rooms
        if user_id in self.user_rooms:
            room_id = self.user_rooms[user_id]
            if room_id in self.room_members:
                self.room_members[room_id].discard(user_id)
                if not self.room_members[room_id]:
                    del self.room_members[room_id]
            del self.user_rooms[user_id]
        
        logger.info(f"User {user_id} disconnected from WebSocket")
        
        # Notify other users about disconnection
        await self.broadcast_user_left(user_id)

    async def send_personal_message(self, message: str, user_id: str):
        """Send a message to a specific user"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message to {user_id}: {e}")
                await self.disconnect(user_id)

    async def send_personal_json(self, data: dict, user_id: str):
        """Send JSON data to a specific user"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(data)
            except Exception as e:
                logger.error(f"Error sending JSON to {user_id}: {e}")
                await self.disconnect(user_id)

    async def broadcast_message(self, message: str, exclude_user: str = None):
        """Broadcast a message to all connected users"""
        disconnected_users = []
        
        for user_id, websocket in list(self.active_connections.items()):
            if exclude_user and user_id == exclude_user:
                continue
                
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {user_id}: {e}")
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            await self.disconnect(user_id)

    async def broadcast_json(self, data: dict, exclude_user: str = None):
        """Broadcast JSON data to all connected users"""
        disconnected_users = []
        
        for user_id, websocket in list(self.active_connections.items()):
            if exclude_user and user_id == exclude_user:
                continue
                
            try:
                await websocket.send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting JSON to {user_id}: {e}")
                disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            await self.disconnect(user_id)

    async def broadcast_to_room(self, data: dict, room_id: str, exclude_user: str = None):
        """Broadcast a message to all users in a specific room"""
        if room_id not in self.room_members:
            return
        
        disconnected_users = []
        
        for user_id in list(self.room_members.get(room_id, set())):
            if exclude_user and user_id == exclude_user:
                continue
                
            if user_id in self.active_connections:
                try:
                    await self.active_connections[user_id].send_json(data)
                except Exception as e:
                    logger.error(f"Error broadcasting to room {room_id}, user {user_id}: {e}")
                    disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            await self.disconnect(user_id)

    async def join_room(self, user_id: str, room_id: str):
        """Add a user to a room"""
        if room_id not in self.room_members:
            self.room_members[room_id] = set()
        
        self.room_members[room_id].add(user_id)
        self.user_rooms[user_id] = room_id
        
        logger.info(f"User {user_id} joined room {room_id}")

    async def leave_room(self, user_id: str, room_id: str):
        """Remove a user from a room"""
        if room_id in self.room_members:
            self.room_members[room_id].discard(user_id)
            if not self.room_members[room_id]:
                del self.room_members[room_id]
        
        if user_id in self.user_rooms and self.user_rooms[user_id] == room_id:
            del self.user_rooms[user_id]
        
        logger.info(f"User {user_id} left room {room_id}")

    async def broadcast_user_joined(self, user_id: str):
        """Notify all users that someone joined"""
        user_info = self.connected_users.get(user_id, {})
        data = {
            "type": "user_joined",
            "user_id": user_id,
            "username": user_info.get("username", user_id),
            "display_name": user_info.get("display_name", user_id),
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_json(data, exclude_user=user_id)

    async def broadcast_user_left(self, user_id: str):
        """Notify all users that someone left"""
        data = {
            "type": "user_left",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_json(data)

    async def send_online_users(self, user_id: str):
        """Send list of online users to a specific user"""
        online_users = [
            {
                "id": uid,
                "username": info.get("username", uid),
                "display_name": info.get("display_name", uid)
            }
            for uid, info in self.connected_users.items()
        ]
        
        data = {
            "type": "online_users",
            "users": online_users,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_personal_json(data, user_id)

    def get_connected_users(self) -> List[dict]:
        """Get list of all connected users"""
        return [
            {
                "id": user_id,
                "username": info.get("username", user_id),
                "display_name": info.get("display_name", user_id),
                "connected_at": info.get("connected_at")
            }
            for user_id, info in self.connected_users.items()
        ]

    def get_room_members(self, room_id: str) -> List[str]:
        """Get list of users in a specific room"""
        return list(self.room_members.get(room_id, set()))

    def is_user_online(self, user_id: str) -> bool:
        """Check if a user is currently online"""
        return user_id in self.active_connections

# Global connection manager instance
manager = ConnectionManager()
