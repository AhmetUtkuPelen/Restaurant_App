"""
Search Service
Handles message search functionality with advanced filtering
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from typing import List, Dict, Optional
from Models.database_models import MessageDB, UserDB, ChatRoomDB, AttachmentDB
from datetime import datetime, timedelta
import re

class SearchService:
    
    @staticmethod
    def search_messages(
        db: Session,
        query: str,
        user_id: str = None,
        room_id: str = None,
        sender_id: str = None,
        message_type: str = None,
        date_from: datetime = None,
        date_to: datetime = None,
        has_attachments: bool = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict:
        """Advanced message search with multiple filters"""
        
        # Base query
        base_query = db.query(MessageDB).filter(MessageDB.is_deleted == False)
        
        # Text search in message content
        if query:
            # Use LIKE for simple text search (can be enhanced with full-text search)
            base_query = base_query.filter(
                MessageDB.content.ilike(f"%{query}%")
            )
        
        # Filter by room
        if room_id:
            base_query = base_query.filter(MessageDB.chat_id == room_id)
        
        # Filter by sender
        if sender_id:
            base_query = base_query.filter(MessageDB.sender_id == sender_id)
        
        # Filter by message type
        if message_type:
            base_query = base_query.filter(MessageDB.message_type == message_type)
        
        # Date range filter
        if date_from:
            base_query = base_query.filter(MessageDB.created_at >= date_from)
        if date_to:
            base_query = base_query.filter(MessageDB.created_at <= date_to)
        
        # Filter messages with attachments
        if has_attachments is not None:
            if has_attachments:
                base_query = base_query.join(AttachmentDB)
            else:
                base_query = base_query.outerjoin(AttachmentDB).filter(
                    AttachmentDB.id.is_(None)
                )
        
        # Get total count
        total_count = base_query.count()
        
        # Apply pagination and ordering
        messages = base_query.order_by(
            MessageDB.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        # Format results
        results = []
        for message in messages:
            # Get sender info
            sender = db.query(UserDB).filter(UserDB.id == message.sender_id).first()
            
            # Get room info if it's a room message
            room = None
            if message.chat_id:
                room = db.query(ChatRoomDB).filter(ChatRoomDB.id == message.chat_id).first()
            
            # Get attachments
            attachments = db.query(AttachmentDB).filter(
                AttachmentDB.message_id == message.id
            ).all()
            
            # Highlight search terms in content
            highlighted_content = SearchService.highlight_search_terms(
                message.content, query
            ) if query else message.content
            
            results.append({
                "id": message.id,
                "content": message.content,
                "highlighted_content": highlighted_content,
                "message_type": message.message_type,
                "created_at": message.created_at,
                "is_edited": message.is_edited,
                "sender": {
                    "id": sender.id,
                    "username": sender.username,
                    "display_name": sender.display_name
                } if sender else None,
                "room": {
                    "id": room.id,
                    "name": room.name
                } if room else None,
                "attachments": [
                    {
                        "id": att.id,
                        "filename": att.original_filename,
                        "file_size": att.file_size,
                        "mime_type": att.mime_type,
                        "attachment_type": att.attachment_type
                    }
                    for att in attachments
                ]
            })
        
        return {
            "results": results,
            "total_count": total_count,
            "page_size": limit,
            "offset": offset,
            "has_more": total_count > (offset + limit)
        }
    
    @staticmethod
    def highlight_search_terms(content: str, query: str) -> str:
        """Highlight search terms in content"""
        if not query or not content:
            return content
        
        # Simple highlighting - wrap matches in <mark> tags
        # In a real app, you might want more sophisticated highlighting
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return pattern.sub(f'<mark>{query}</mark>', content)
    
    @staticmethod
    def search_users(db: Session, query: str, limit: int = 20) -> List[Dict]:
        """Search for users by username or display name"""
        
        users = db.query(UserDB).filter(
            or_(
                UserDB.username.ilike(f"%{query}%"),
                UserDB.display_name.ilike(f"%{query}%"),
                UserDB.email.ilike(f"%{query}%")
            )
        ).filter(UserDB.is_active == True).limit(limit).all()
        
        return [
            {
                "id": user.id,
                "username": user.username,
                "display_name": user.display_name,
                "email": user.email,
                "status": user.status
            }
            for user in users
        ]
    
    @staticmethod
    def search_rooms(db: Session, query: str, user_id: str = None, limit: int = 20) -> List[Dict]:
        """Search for chat rooms"""
        
        base_query = db.query(ChatRoomDB).filter(
            or_(
                ChatRoomDB.name.ilike(f"%{query}%"),
                ChatRoomDB.description.ilike(f"%{query}%")
            )
        )
        
        # Only show public rooms or rooms the user is a member of
        if user_id:
            from Models.database_models import ChatMemberDB
            base_query = base_query.filter(
                or_(
                    ChatRoomDB.is_private == False,
                    ChatRoomDB.id.in_(
                        db.query(ChatMemberDB.chat_id).filter(
                            ChatMemberDB.user_id == user_id
                        )
                    )
                )
            )
        else:
            base_query = base_query.filter(ChatRoomDB.is_private == False)
        
        rooms = base_query.limit(limit).all()
        
        result = []
        for room in rooms:
            # Get member count
            from Models.database_models import ChatMemberDB
            member_count = db.query(ChatMemberDB).filter(
                ChatMemberDB.chat_id == room.id
            ).count()
            
            # Check if user is a member
            is_member = False
            if user_id:
                is_member = db.query(ChatMemberDB).filter(
                    and_(
                        ChatMemberDB.chat_id == room.id,
                        ChatMemberDB.user_id == user_id
                    )
                ).first() is not None
            
            result.append({
                "id": room.id,
                "name": room.name,
                "description": room.description,
                "is_private": room.is_private,
                "member_count": member_count,
                "is_member": is_member,
                "created_at": room.created_at
            })
        
        return result
    
    @staticmethod
    def get_search_suggestions(db: Session, query: str, user_id: str = None) -> Dict:
        """Get search suggestions for autocomplete"""
        
        suggestions = {
            "messages": [],
            "users": [],
            "rooms": []
        }
        
        if len(query) >= 2:  # Only suggest for queries with 2+ characters
            # Message content suggestions (recent unique phrases)
            message_suggestions = db.query(MessageDB.content).filter(
                MessageDB.content.ilike(f"%{query}%"),
                MessageDB.is_deleted == False
            ).distinct().limit(5).all()
            
            suggestions["messages"] = [
                msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                for msg in message_suggestions
            ]
            
            # User suggestions
            user_suggestions = SearchService.search_users(db, query, limit=5)
            suggestions["users"] = user_suggestions
            
            # Room suggestions
            room_suggestions = SearchService.search_rooms(db, query, user_id, limit=5)
            suggestions["rooms"] = room_suggestions
        
        return suggestions
    
    @staticmethod
    def get_popular_search_terms(db: Session, days: int = 7, limit: int = 10) -> List[str]:
        """Get popular search terms (this would require search logging)"""
        # This is a placeholder - in a real app, you'd log search queries
        # and return the most popular ones
        
        # For now, return some common search patterns based on message content
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get most common words from recent messages
        recent_messages = db.query(MessageDB.content).filter(
            MessageDB.created_at >= cutoff_date,
            MessageDB.is_deleted == False
        ).all()
        
        # Simple word frequency analysis
        word_freq = {}
        for message in recent_messages:
            if message.content:
                words = re.findall(r'\b\w{3,}\b', message.content.lower())
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top words
        popular_terms = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [term[0] for term in popular_terms[:limit]]
    
    @staticmethod
    def search_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        user_id: str = None,
        room_id: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """Search messages within a specific date range"""
        
        query = db.query(MessageDB).filter(
            MessageDB.created_at >= start_date,
            MessageDB.created_at <= end_date,
            MessageDB.is_deleted == False
        )
        
        if user_id:
            query = query.filter(MessageDB.sender_id == user_id)
        
        if room_id:
            query = query.filter(MessageDB.chat_id == room_id)
        
        messages = query.order_by(MessageDB.created_at.desc()).limit(limit).all()
        
        results = []
        for message in messages:
            sender = db.query(UserDB).filter(UserDB.id == message.sender_id).first()
            
            results.append({
                "id": message.id,
                "content": message.content,
                "created_at": message.created_at,
                "sender": {
                    "id": sender.id,
                    "username": sender.username,
                    "display_name": sender.display_name
                } if sender else None
            })
        
        return results
    
    @staticmethod
    def search_attachments(
        db: Session,
        filename_query: str = None,
        file_type: str = None,
        user_id: str = None,
        limit: int = 50
    ) -> List[Dict]:
        """Search for file attachments"""
        
        query = db.query(AttachmentDB)
        
        if filename_query:
            query = query.filter(
                AttachmentDB.original_filename.ilike(f"%{filename_query}%")
            )
        
        if file_type:
            query = query.filter(AttachmentDB.attachment_type == file_type)
        
        if user_id:
            # Join with messages to filter by sender
            query = query.join(MessageDB).filter(MessageDB.sender_id == user_id)
        
        attachments = query.order_by(AttachmentDB.created_at.desc()).limit(limit).all()
        
        results = []
        for attachment in attachments:
            # Get message info
            message = db.query(MessageDB).filter(
                MessageDB.id == attachment.message_id
            ).first()
            
            sender = None
            if message:
                sender = db.query(UserDB).filter(UserDB.id == message.sender_id).first()
            
            results.append({
                "id": attachment.id,
                "filename": attachment.original_filename,
                "file_size": attachment.file_size,
                "mime_type": attachment.mime_type,
                "attachment_type": attachment.attachment_type,
                "url": attachment.url,
                "created_at": attachment.created_at,
                "message_id": attachment.message_id,
                "sender": {
                    "id": sender.id,
                    "username": sender.username,
                    "display_name": sender.display_name
                } if sender else None
            })
        
        return results
