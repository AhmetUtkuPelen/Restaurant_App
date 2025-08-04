"""
Soft Delete Service for managing soft deletion functionality.
This service provides utilities for soft deleting records and querying non-deleted records.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Type, Optional, List
from database import Base

class SoftDeleteService:
    """Service for handling soft delete operations."""
    
    @staticmethod
    def soft_delete(db: Session, model_instance: Base) -> bool:
        """
        Soft delete a model instance by setting is_deleted=True and deleted_at=now().
        
        Args:
            db: Database session
            model_instance: The model instance to soft delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if hasattr(model_instance, 'is_deleted') and hasattr(model_instance, 'deleted_at'):
                model_instance.is_deleted = True
                model_instance.deleted_at = datetime.utcnow()
                db.commit()
                return True
            else:
                raise ValueError(f"Model {type(model_instance).__name__} does not support soft delete")
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def restore(db: Session, model_instance: Base) -> bool:
        """
        Restore a soft deleted model instance.
        
        Args:
            db: Database session
            model_instance: The model instance to restore
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if hasattr(model_instance, 'is_deleted') and hasattr(model_instance, 'deleted_at'):
                model_instance.is_deleted = False
                model_instance.deleted_at = None
                db.commit()
                return True
            else:
                raise ValueError(f"Model {type(model_instance).__name__} does not support soft delete")
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_active_query(db: Session, model_class: Type[Base]):
        """
        Get a query for active (non-deleted) records.
        
        Args:
            db: Database session
            model_class: The model class to query
            
        Returns:
            Query object filtered for active records
        """
        if hasattr(model_class, 'is_deleted'):
            return db.query(model_class).filter(model_class.is_deleted == False)
        else:
            return db.query(model_class)
    
    @staticmethod
    def get_deleted_query(db: Session, model_class: Type[Base]):
        """
        Get a query for deleted records.
        
        Args:
            db: Database session
            model_class: The model class to query
            
        Returns:
            Query object filtered for deleted records
        """
        if hasattr(model_class, 'is_deleted'):
            return db.query(model_class).filter(model_class.is_deleted == True)
        else:
            return db.query(model_class).filter(False)  # Return empty query
    
    @staticmethod
    def get_all_query(db: Session, model_class: Type[Base]):
        """
        Get a query for all records (including deleted).
        
        Args:
            db: Database session
            model_class: The model class to query
            
        Returns:
            Query object for all records
        """
        return db.query(model_class)
    
    @staticmethod
    def permanent_delete(db: Session, model_instance: Base) -> bool:
        """
        Permanently delete a model instance from the database.
        
        Args:
            db: Database session
            model_instance: The model instance to permanently delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            db.delete(model_instance)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def cleanup_deleted_records(db: Session, model_class: Type[Base], days_old: int = 30) -> int:
        """
        Permanently delete soft-deleted records older than specified days.
        
        Args:
            db: Database session
            model_class: The model class to clean up
            days_old: Number of days old records should be before permanent deletion
            
        Returns:
            int: Number of records permanently deleted
        """
        if not hasattr(model_class, 'is_deleted') or not hasattr(model_class, 'deleted_at'):
            return 0
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            # Find records to delete
            records_to_delete = db.query(model_class).filter(
                and_(
                    model_class.is_deleted == True,
                    model_class.deleted_at < cutoff_date
                )
            ).all()
            
            count = len(records_to_delete)
            
            # Permanently delete them
            for record in records_to_delete:
                db.delete(record)
            
            db.commit()
            return count
            
        except Exception as e:
            db.rollback()
            raise e

class SoftDeleteMixin:
    """
    Mixin class to add soft delete functionality to models.
    Add this to your model classes to enable soft delete.
    """
    
    def soft_delete(self, db: Session) -> bool:
        """Soft delete this instance."""
        return SoftDeleteService.soft_delete(db, self)
    
    def restore(self, db: Session) -> bool:
        """Restore this soft deleted instance."""
        return SoftDeleteService.restore(db, self)
    
    def permanent_delete(self, db: Session) -> bool:
        """Permanently delete this instance."""
        return SoftDeleteService.permanent_delete(db, self)
    
    @property
    def is_active(self) -> bool:
        """Check if this instance is active (not soft deleted)."""
        return not getattr(self, 'is_deleted', False)
    
    @classmethod
    def get_active(cls, db: Session):
        """Get query for active (non-deleted) records of this model."""
        return SoftDeleteService.get_active_query(db, cls)
    
    @classmethod
    def get_deleted(cls, db: Session):
        """Get query for deleted records of this model."""
        return SoftDeleteService.get_deleted_query(db, cls)
    
    @classmethod
    def get_all(cls, db: Session):
        """Get query for all records (including deleted) of this model."""
        return SoftDeleteService.get_all_query(db, cls)