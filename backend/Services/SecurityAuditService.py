"""
Security Audit Service for comprehensive security tracking and logging.
This service provides utilities for creating audit logs and analyzing security events.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from Models.database_models import AuditLogDB
import json

class SecurityAuditService:
    """Service for handling audit logging and security tracking."""
    
    # Risk levels
    RISK_LOW = "low"
    RISK_MEDIUM = "medium"
    RISK_HIGH = "high"
    RISK_CRITICAL = "critical"
    
    # Common actions
    ACTION_LOGIN = "login"
    ACTION_LOGOUT = "logout"
    ACTION_REGISTER = "register"
    ACTION_PASSWORD_CHANGE = "password_change"
    ACTION_PASSWORD_RESET = "password_reset"
    ACTION_PROFILE_UPDATE = "profile_update"
    ACTION_MESSAGE_SEND = "message_send"
    ACTION_MESSAGE_DELETE = "message_delete"
    ACTION_FILE_UPLOAD = "file_upload"
    ACTION_ADMIN_ACCESS = "admin_access"
    ACTION_DATA_EXPORT = "data_export"
    ACTION_ACCOUNT_LOCK = "account_lock"
    ACTION_ACCOUNT_UNLOCK = "account_unlock"
    
    # Resource types
    RESOURCE_USER = "user"
    RESOURCE_MESSAGE = "message"
    RESOURCE_FILE = "file"
    RESOURCE_CHAT_ROOM = "chat_room"
    RESOURCE_SYSTEM = "system"
    
    @staticmethod
    def log_action(
        db: Session,
        action: str,
        resource_type: str,
        user_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        risk_level: str = RISK_LOW
    ) -> AuditLogDB:
        """
        Log an action to the audit trail.
        """
        return AuditLogDB.create_log(
            db=db,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            request_id=request_id,
            success=success,
            error_message=error_message,
            risk_level=risk_level
        )
    
    @staticmethod
    def log_login_attempt(
        db: Session,
        user_id: Optional[str],
        username: str,
        success: bool,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        error_message: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> AuditLogDB:
        """Log a login attempt."""
        risk_level = SecurityAuditService.RISK_LOW if success else SecurityAuditService.RISK_MEDIUM
        
        details = {
            "username": username,
            "login_method": "password"
        }
        
        return SecurityAuditService.log_action(
            db=db,
            action=SecurityAuditService.ACTION_LOGIN,
            resource_type=SecurityAuditService.RESOURCE_USER,
            user_id=user_id,
            resource_id=user_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            request_id=request_id,
            success=success,
            error_message=error_message,
            risk_level=risk_level
        )
    
    @staticmethod
    def log_password_change(
        db: Session,
        user_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        forced: bool = False
    ) -> AuditLogDB:
        """Log a password change event."""
        details = {
            "forced": forced,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        risk_level = SecurityAuditService.RISK_HIGH if forced else SecurityAuditService.RISK_MEDIUM
        
        return SecurityAuditService.log_action(
            db=db,
            action=SecurityAuditService.ACTION_PASSWORD_CHANGE,
            resource_type=SecurityAuditService.RESOURCE_USER,
            user_id=user_id,
            resource_id=user_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            request_id=request_id,
            success=True,
            risk_level=risk_level
        )
    
    @staticmethod
    def get_failed_login_attempts(
        db: Session,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        hours: int = 24
    ) -> List[AuditLogDB]:
        """Get failed login attempts for analysis."""
        return AuditLogDB.get_failed_attempts(db, user_id, ip_address, hours)
    
    @staticmethod
    def get_user_activity(
        db: Session,
        user_id: str,
        limit: int = 50
    ) -> List[AuditLogDB]:
        """Get recent activity for a specific user."""
        return AuditLogDB.get_user_activity(db, user_id, limit)
    
    @staticmethod
    def analyze_suspicious_activity(
        db: Session,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        hours: int = 24
    ) -> Dict[str, Any]:
        """
        Analyze suspicious activity patterns.
        
        Returns:
            Dict containing analysis results
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = db.query(AuditLogDB).filter(AuditLogDB.timestamp >= cutoff_time)
        
        if user_id:
            query = query.filter(AuditLogDB.user_id == user_id)
        if ip_address:
            query = query.filter(AuditLogDB.ip_address == ip_address)
        
        events = query.all()
        
        # Analyze patterns
        failed_logins = len([e for e in events if e.action == SecurityAuditService.ACTION_LOGIN and not e.success])
        high_risk_events = len([e for e in events if e.risk_level in [SecurityAuditService.RISK_HIGH, SecurityAuditService.RISK_CRITICAL]])
        unique_ips = len(set([e.ip_address for e in events if e.ip_address]))
        
        # Calculate risk score
        risk_score = 0
        risk_score += failed_logins * 2
        risk_score += high_risk_events * 5
        risk_score += max(0, unique_ips - 3) * 3  # Multiple IPs can be suspicious
        
        return {
            "total_events": len(events),
            "failed_logins": failed_logins,
            "high_risk_events": high_risk_events,
            "unique_ips": unique_ips,
            "risk_score": risk_score,
            "risk_level": (
                SecurityAuditService.RISK_CRITICAL if risk_score >= 20 else
                SecurityAuditService.RISK_HIGH if risk_score >= 10 else
                SecurityAuditService.RISK_MEDIUM if risk_score >= 5 else
                SecurityAuditService.RISK_LOW
            ),
            "analysis_period_hours": hours,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }