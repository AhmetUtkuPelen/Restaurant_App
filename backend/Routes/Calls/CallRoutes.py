"""
Call Routes
API endpoints for voice and video calling
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel

from database import get_db
from Services.CallService import CallService
from Services.WebSocketManager import manager

router = APIRouter(prefix="/calls", tags=["calls"])

# Pydantic models
class CallInitiate(BaseModel):
    call_type: str  # "audio" or "video"
    room_id: Optional[str] = None
    participant_ids: Optional[List[str]] = None

class CallResponse(BaseModel):
    call_id: str
    action: str

@router.post("/initiate")
async def initiate_call(
    call_data: CallInitiate,
    caller_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Initiate a new call"""
    
    try:
        if call_data.call_type not in ["audio", "video"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Call type must be 'audio' or 'video'"
            )
        
        call = CallService.initiate_call(
            db=db,
            caller_id=caller_id,
            call_type=call_data.call_type,
            room_id=call_data.room_id,
            participant_ids=call_data.participant_ids
        )
        
        return {
            "success": True,
            "call": {
                "id": call.id,
                "call_type": call.call_type,
                "status": call.status,
                "room_id": call.room_id,
                "started_at": call.started_at.isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate call: {str(e)}"
        )

@router.post("/{call_id}/join")
async def join_call(
    call_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Join an existing call"""
    
    try:
        success = CallService.join_call(db, call_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to join call. Call may not exist or user not invited."
            )
        
        return {
            "success": True,
            "message": "Successfully joined call",
            "call_id": call_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to join call: {str(e)}"
        )

@router.post("/{call_id}/leave")
async def leave_call(
    call_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Leave a call"""
    
    try:
        success = CallService.leave_call(db, call_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to leave call. User may not be in the call."
            )
        
        return {
            "success": True,
            "message": "Successfully left call"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to leave call: {str(e)}"
        )

@router.post("/{call_id}/reject")
async def reject_call(
    call_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Reject a call invitation"""
    
    try:
        success = CallService.reject_call(db, call_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to reject call. Call may not exist or user not invited."
            )
        
        return {
            "success": True,
            "message": "Call rejected"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reject call: {str(e)}"
        )

@router.post("/{call_id}/end")
async def end_call(
    call_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """End a call (caller or admin only)"""
    
    try:
        success = CallService.end_call(db, call_id, user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the caller or room admin can end the call"
            )
        
        return {
            "success": True,
            "message": "Call ended"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to end call: {str(e)}"
        )

@router.get("/active/{user_id}")
async def get_active_calls(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get active calls for a user"""
    
    try:
        calls = CallService.get_active_calls(db, user_id)
        
        return {
            "success": True,
            "user_id": user_id,
            "active_calls": calls,
            "count": len(calls)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active calls: {str(e)}"
        )

@router.get("/history/{user_id}")
async def get_call_history(
    user_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get call history for a user"""
    
    try:
        history = CallService.get_call_history(db, user_id, limit)
        
        return {
            "success": True,
            "user_id": user_id,
            "call_history": history,
            "count": len(history)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get call history: {str(e)}"
        )

@router.post("/{call_id}/signal")
async def send_call_signal(
    call_id: str,
    signal_data: Dict,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Send WebRTC signaling data"""
    
    try:
        # Broadcast signaling data to other call participants
        signaling_message = {
            "type": "webrtc_signal",
            "call_id": call_id,
            "from_user": user_id,
            "signal_data": signal_data
        }
        
        # Send to all participants except sender
        await manager.broadcast_to_room(signaling_message, call_id, exclude_user=user_id)
        
        return {
            "success": True,
            "message": "Signal sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send signal: {str(e)}"
        )

@router.post("/{call_id}/ice-candidate")
async def send_ice_candidate(
    call_id: str,
    candidate_data: Dict,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Send ICE candidate for WebRTC connection"""
    
    try:
        ice_message = {
            "type": "ice_candidate",
            "call_id": call_id,
            "from_user": user_id,
            "candidate": candidate_data
        }
        
        # Send to all participants except sender
        await manager.broadcast_to_room(ice_message, call_id, exclude_user=user_id)
        
        return {
            "success": True,
            "message": "ICE candidate sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send ICE candidate: {str(e)}"
        )

@router.post("/{call_id}/offer")
async def send_offer(
    call_id: str,
    offer_data: Dict,
    target_user_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Send WebRTC offer to specific user"""
    
    try:
        offer_message = {
            "type": "webrtc_offer",
            "call_id": call_id,
            "from_user": user_id,
            "offer": offer_data
        }
        
        # Send to specific user
        await manager.send_personal_json(offer_message, target_user_id)
        
        return {
            "success": True,
            "message": "Offer sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send offer: {str(e)}"
        )

@router.post("/{call_id}/answer")
async def send_answer(
    call_id: str,
    answer_data: Dict,
    target_user_id: str,
    user_id: str,  # In real app, get from JWT token
    db: Session = Depends(get_db)
):
    """Send WebRTC answer to specific user"""
    
    try:
        answer_message = {
            "type": "webrtc_answer",
            "call_id": call_id,
            "from_user": user_id,
            "answer": answer_data
        }
        
        # Send to specific user
        await manager.send_personal_json(answer_message, target_user_id)
        
        return {
            "success": True,
            "message": "Answer sent"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send answer: {str(e)}"
        )
