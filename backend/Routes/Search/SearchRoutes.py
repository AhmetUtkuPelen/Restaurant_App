"""
Search Routes
API endpoints for search functionality
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

from database import get_db
from Services.SearchService import SearchService

router = APIRouter(prefix="/search", tags=["search"])

# Pydantic models
class MessageSearchParams(BaseModel):
    query: str = ""
    room_id: Optional[str] = None
    sender_id: Optional[str] = None
    message_type: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    has_attachments: Optional[bool] = None
    limit: int = 50
    offset: int = 0

@router.get("/messages")
async def search_messages(
    query: str = Query("", description="Search query"),
    user_id: str = Query(..., description="User ID for authorization"),
    room_id: Optional[str] = Query(None, description="Filter by room"),
    sender_id: Optional[str] = Query(None, description="Filter by sender"),
    message_type: Optional[str] = Query(None, description="Filter by message type"),
    date_from: Optional[datetime] = Query(None, description="Start date"),
    date_to: Optional[datetime] = Query(None, description="End date"),
    has_attachments: Optional[bool] = Query(None, description="Filter messages with attachments"),
    limit: int = Query(50, description="Number of results per page"),
    offset: int = Query(0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """Search messages with advanced filtering"""
    
    try:
        results = SearchService.search_messages(
            db=db,
            query=query,
            user_id=user_id,
            room_id=room_id,
            sender_id=sender_id,
            message_type=message_type,
            date_from=date_from,
            date_to=date_to,
            has_attachments=has_attachments,
            limit=limit,
            offset=offset
        )
        
        return {
            "success": True,
            "search_query": query,
            "filters": {
                "room_id": room_id,
                "sender_id": sender_id,
                "message_type": message_type,
                "date_from": date_from,
                "date_to": date_to,
                "has_attachments": has_attachments
            },
            **results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/users")
async def search_users(
    query: str = Query(..., description="Search query for users"),
    limit: int = Query(20, description="Number of results"),
    db: Session = Depends(get_db)
):
    """Search for users by username, display name, or email"""
    
    try:
        users = SearchService.search_users(db, query, limit)
        
        return {
            "success": True,
            "query": query,
            "results": users,
            "count": len(users)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"User search failed: {str(e)}"
        )

@router.get("/rooms")
async def search_rooms(
    query: str = Query(..., description="Search query for rooms"),
    user_id: Optional[str] = Query(None, description="User ID for filtering"),
    limit: int = Query(20, description="Number of results"),
    db: Session = Depends(get_db)
):
    """Search for chat rooms"""
    
    try:
        rooms = SearchService.search_rooms(db, query, user_id, limit)
        
        return {
            "success": True,
            "query": query,
            "results": rooms,
            "count": len(rooms)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Room search failed: {str(e)}"
        )

@router.get("/suggestions")
async def get_search_suggestions(
    query: str = Query(..., description="Partial search query"),
    user_id: Optional[str] = Query(None, description="User ID for personalization"),
    db: Session = Depends(get_db)
):
    """Get search suggestions for autocomplete"""
    
    try:
        suggestions = SearchService.get_search_suggestions(db, query, user_id)
        
        return {
            "success": True,
            "query": query,
            "suggestions": suggestions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get suggestions: {str(e)}"
        )

@router.get("/popular-terms")
async def get_popular_search_terms(
    days: int = Query(7, description="Number of days to look back"),
    limit: int = Query(10, description="Number of terms to return"),
    db: Session = Depends(get_db)
):
    """Get popular search terms"""
    
    try:
        terms = SearchService.get_popular_search_terms(db, days, limit)
        
        return {
            "success": True,
            "popular_terms": terms,
            "period_days": days
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get popular terms: {str(e)}"
        )

@router.get("/by-date-range")
async def search_by_date_range(
    start_date: datetime = Query(..., description="Start date"),
    end_date: datetime = Query(..., description="End date"),
    user_id: Optional[str] = Query(None, description="Filter by user"),
    room_id: Optional[str] = Query(None, description="Filter by room"),
    limit: int = Query(100, description="Number of results"),
    db: Session = Depends(get_db)
):
    """Search messages within a specific date range"""
    
    try:
        messages = SearchService.search_by_date_range(
            db=db,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            room_id=room_id,
            limit=limit
        )
        
        return {
            "success": True,
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "filters": {
                "user_id": user_id,
                "room_id": room_id
            },
            "results": messages,
            "count": len(messages)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Date range search failed: {str(e)}"
        )

@router.get("/attachments")
async def search_attachments(
    filename_query: Optional[str] = Query(None, description="Search in filenames"),
    file_type: Optional[str] = Query(None, description="Filter by file type"),
    user_id: Optional[str] = Query(None, description="Filter by uploader"),
    limit: int = Query(50, description="Number of results"),
    db: Session = Depends(get_db)
):
    """Search for file attachments"""
    
    try:
        attachments = SearchService.search_attachments(
            db=db,
            filename_query=filename_query,
            file_type=file_type,
            user_id=user_id,
            limit=limit
        )
        
        return {
            "success": True,
            "filters": {
                "filename_query": filename_query,
                "file_type": file_type,
                "user_id": user_id
            },
            "results": attachments,
            "count": len(attachments)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Attachment search failed: {str(e)}"
        )

@router.post("/advanced")
async def advanced_search(
    search_params: MessageSearchParams,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Advanced search with complex parameters"""
    
    try:
        results = SearchService.search_messages(
            db=db,
            query=search_params.query,
            user_id=user_id,
            room_id=search_params.room_id,
            sender_id=search_params.sender_id,
            message_type=search_params.message_type,
            date_from=search_params.date_from,
            date_to=search_params.date_to,
            has_attachments=search_params.has_attachments,
            limit=search_params.limit,
            offset=search_params.offset
        )
        
        return {
            "success": True,
            "search_params": search_params.dict(),
            **results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Advanced search failed: {str(e)}"
        )

@router.get("/global")
async def global_search(
    query: str = Query(..., description="Global search query"),
    user_id: str = Query(..., description="User ID for authorization"),
    limit: int = Query(20, description="Results per category"),
    db: Session = Depends(get_db)
):
    """Global search across messages, users, and rooms"""
    
    try:
        # Search in all categories
        message_results = SearchService.search_messages(
            db=db,
            query=query,
            user_id=user_id,
            limit=limit
        )
        
        user_results = SearchService.search_users(db, query, limit)
        room_results = SearchService.search_rooms(db, query, user_id, limit)
        
        return {
            "success": True,
            "query": query,
            "results": {
                "messages": {
                    "results": message_results["results"],
                    "total_count": message_results["total_count"]
                },
                "users": {
                    "results": user_results,
                    "count": len(user_results)
                },
                "rooms": {
                    "results": room_results,
                    "count": len(room_results)
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Global search failed: {str(e)}"
        )
