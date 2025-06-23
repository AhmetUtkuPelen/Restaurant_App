"""
Chat Room Service
Handles chat rooms/channels functionality
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Dict, Optional
from Models.database_models import ChatRoomDB, ChatMemberDB, UserDB, MessageDB
from datetime import datetime
import uuid
import json

class RoomService:
    
    @staticmethod
    def create_room(db: Session, name: str, description: str, created_by: str, is_private: bool = False) -> ChatRoomDB:
        """Create a new chat room"""
        
        room = ChatRoomDB(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            is_private=is_private,
            created_by=created_by,
            members=[created_by],  # Creator is automatically a member
            admins=[created_by]    # Creator is automatically an admin
        )
        
        db.add(room)
        db.commit()
        db.refresh(room)
        
        # Add creator as a member in the members table
        member = ChatMemberDB(
            id=str(uuid.uuid4()),
            chat_id=room.id,
            user_id=created_by,
            is_admin=True
        )
        
        db.add(member)
        db.commit()
        
        return room
    
    @staticmethod
    def get_room_by_id(db: Session, room_id: str) -> Optional[ChatRoomDB]:
        """Get a room by its ID"""
        return db.query(ChatRoomDB).filter(ChatRoomDB.id == room_id).first()
    
    @staticmethod
    def get_user_rooms(db: Session, user_id: str) -> List[Dict]:
        """Get all rooms that a user is a member of"""
        
        # Get rooms where user is a member
        member_rooms = db.query(ChatRoomDB).join(ChatMemberDB).filter(
            ChatMemberDB.user_id == user_id
        ).all()
        
        result = []
        for room in member_rooms:
            # Get member info for this user
            member = db.query(ChatMemberDB).filter(
                and_(ChatMemberDB.chat_id == room.id, ChatMemberDB.user_id == user_id)
            ).first()
            
            # Get latest message
            latest_message = db.query(MessageDB).filter(
                MessageDB.chat_id == room.id
            ).order_by(MessageDB.created_at.desc()).first()
            
            # Get member count
            member_count = db.query(ChatMemberDB).filter(
                ChatMemberDB.chat_id == room.id
            ).count()
            
            result.append({
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "is_private": room.is_private,
                "created_by": room.created_by,
                "created_at": room.created_at,
                "member_count": member_count,
                "user_role": "admin" if member and member.is_admin else "member",
                "is_muted": member.is_muted if member else False,
                "joined_at": member.joined_at if member else None,
                "latest_message": {
                    "content": latest_message.content,
                    "sender_id": latest_message.sender_id,
                    "created_at": latest_message.created_at
                } if latest_message else None
            })
        
        return result
    
    @staticmethod
    def get_public_rooms(db: Session, limit: int = 50) -> List[Dict]:
        """Get all public rooms"""
        
        rooms = db.query(ChatRoomDB).filter(
            ChatRoomDB.is_private == False
        ).order_by(ChatRoomDB.created_at.desc()).limit(limit).all()
        
        result = []
        for room in rooms:
            member_count = db.query(ChatMemberDB).filter(
                ChatMemberDB.chat_id == room.id
            ).count()
            
            creator = db.query(UserDB).filter(UserDB.id == room.created_by).first()
            
            result.append({
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "created_by": room.created_by,
                "creator_name": creator.display_name if creator else "Unknown",
                "created_at": room.created_at,
                "member_count": member_count
            })
        
        return result
    
    @staticmethod
    def join_room(db: Session, room_id: str, user_id: str) -> bool:
        """Add a user to a room"""
        
        # Check if user is already a member
        existing_member = db.query(ChatMemberDB).filter(
            and_(ChatMemberDB.chat_id == room_id, ChatMemberDB.user_id == user_id)
        ).first()
        
        if existing_member:
            return False  # Already a member
        
        # Check if room exists
        room = db.query(ChatRoomDB).filter(ChatRoomDB.id == room_id).first()
        if not room:
            return False
        
        # Add to members table
        member = ChatMemberDB(
            id=str(uuid.uuid4()),
            chat_id=room_id,
            user_id=user_id,
            is_admin=False
        )
        
        db.add(member)
        
        # Update room members list
        current_members = room.members or []
        if user_id not in current_members:
            current_members.append(user_id)
            room.members = current_members
        
        db.commit()
        return True
    
    @staticmethod
    def leave_room(db: Session, room_id: str, user_id: str) -> bool:
        """Remove a user from a room"""
        
        # Remove from members table
        member = db.query(ChatMemberDB).filter(
            and_(ChatMemberDB.chat_id == room_id, ChatMemberDB.user_id == user_id)
        ).first()
        
        if not member:
            return False
        
        db.delete(member)
        
        # Update room members list
        room = db.query(ChatRoomDB).filter(ChatRoomDB.id == room_id).first()
        if room and room.members:
            current_members = room.members
            if user_id in current_members:
                current_members.remove(user_id)
                room.members = current_members
            
            # Also remove from admins if they were an admin
            if room.admins and user_id in room.admins:
                current_admins = room.admins
                current_admins.remove(user_id)
                room.admins = current_admins
        
        db.commit()
        return True
    
    @staticmethod
    def get_room_members(db: Session, room_id: str) -> List[Dict]:
        """Get all members of a room"""
        
        members = db.query(ChatMemberDB, UserDB).join(
            UserDB, ChatMemberDB.user_id == UserDB.id
        ).filter(ChatMemberDB.chat_id == room_id).all()
        
        result = []
        for member, user in members:
            result.append({
                "user_id": user.id,
                "username": user.username,
                "display_name": user.display_name,
                "email": user.email,
                "is_admin": member.is_admin,
                "is_muted": member.is_muted,
                "joined_at": member.joined_at,
                "status": user.status
            })
        
        return result
    
    @staticmethod
    def update_room(db: Session, room_id: str, user_id: str, **updates) -> Optional[ChatRoomDB]:
        """Update room details (only admins can update)"""
        
        # Check if user is admin
        member = db.query(ChatMemberDB).filter(
            and_(
                ChatMemberDB.chat_id == room_id,
                ChatMemberDB.user_id == user_id,
                ChatMemberDB.is_admin == True
            )
        ).first()
        
        if not member:
            return None  # User is not an admin
        
        room = db.query(ChatRoomDB).filter(ChatRoomDB.id == room_id).first()
        if not room:
            return None
        
        # Update allowed fields
        allowed_fields = ['name', 'description', 'is_private']
        for field, value in updates.items():
            if field in allowed_fields:
                setattr(room, field, value)
        
        db.commit()
        db.refresh(room)
        return room
    
    @staticmethod
    def promote_to_admin(db: Session, room_id: str, admin_user_id: str, target_user_id: str) -> bool:
        """Promote a user to admin (only existing admins can do this)"""
        
        # Check if requesting user is admin
        admin_member = db.query(ChatMemberDB).filter(
            and_(
                ChatMemberDB.chat_id == room_id,
                ChatMemberDB.user_id == admin_user_id,
                ChatMemberDB.is_admin == True
            )
        ).first()
        
        if not admin_member:
            return False
        
        # Update target user
        target_member = db.query(ChatMemberDB).filter(
            and_(ChatMemberDB.chat_id == room_id, ChatMemberDB.user_id == target_user_id)
        ).first()
        
        if not target_member:
            return False
        
        target_member.is_admin = True
        
        # Update room admins list
        room = db.query(ChatRoomDB).filter(ChatRoomDB.id == room_id).first()
        if room:
            current_admins = room.admins or []
            if target_user_id not in current_admins:
                current_admins.append(target_user_id)
                room.admins = current_admins
        
        db.commit()
        return True
    
    @staticmethod
    def search_rooms(db: Session, query: str, user_id: str = None) -> List[Dict]:
        """Search for rooms by name or description"""
        
        rooms = db.query(ChatRoomDB).filter(
            or_(
                ChatRoomDB.name.ilike(f"%{query}%"),
                ChatRoomDB.description.ilike(f"%{query}%")
            )
        ).filter(ChatRoomDB.is_private == False).all()
        
        result = []
        for room in rooms:
            member_count = db.query(ChatMemberDB).filter(
                ChatMemberDB.chat_id == room.id
            ).count()
            
            is_member = False
            if user_id:
                is_member = db.query(ChatMemberDB).filter(
                    and_(ChatMemberDB.chat_id == room.id, ChatMemberDB.user_id == user_id)
                ).first() is not None
            
            result.append({
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "created_at": room.created_at,
                "member_count": member_count,
                "is_member": is_member
            })
        
        return result
