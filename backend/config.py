from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # Database Configuration
    database_url: str = "sqlite:///./chat_app.db"
    
    # Security Configuration
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # Password Security
    bcrypt_rounds: int = 12
    
    # File Upload Configuration
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: str = ".jpg,.jpeg,.png,.gif,.pdf,.txt,.doc,.docx"
    
    # Rate Limiting Configuration
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hour
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Development Configuration
    debug: bool = False
    log_level: str = "INFO"
    
    # Email Configuration
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Admin Configuration
    admin_email: str = "admin@example.com"
    admin_username: str = "admin"
    admin_password: str = "admin123"
    
    @field_validator('upload_dir')
    @classmethod
    def create_upload_dir(cls, v):
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get allowed origins as a list"""
        if isinstance(self.allowed_origins, str):
            return [origin.strip() for origin in self.allowed_origins.split(',')]
        return [self.allowed_origins] if self.allowed_origins else []
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        """Get allowed file types as a list"""
        if isinstance(self.allowed_file_types, str):
            return [ext.strip() for ext in self.allowed_file_types.split(',')]
        return [self.allowed_file_types] if self.allowed_file_types else []
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Ensure upload directory exists
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)