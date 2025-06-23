import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException
from PIL import Image
import magic
from typing import Optional, Tuple
from datetime import datetime
import hashlib

class FileHandler:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.max_image_size = 5 * 1024 * 1024   # 5MB for images
        self.allowed_image_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        self.allowed_file_types = {
            "application/pdf", "text/plain", "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
        
        # Create upload directories if they don't exist
        os.makedirs(f"{upload_dir}/images", exist_ok=True)
        os.makedirs(f"{upload_dir}/files", exist_ok=True)
        os.makedirs(f"{upload_dir}/thumbnails", exist_ok=True)

    async def validate_file(self, file: UploadFile) -> Tuple[bool, str]:
        """Validate uploaded file"""
        # Check file size
        file_size = 0
        content = await file.read()
        file_size = len(content)
        await file.seek(0)  # Reset file pointer after reading content
        
        if file_size > self.max_file_size:
            return False, "File size exceeds maximum limit"
        
        # Check MIME type
        mime_type = magic.from_buffer(content, mime=True)
        
        if mime_type.startswith('image/'):
            if mime_type not in self.allowed_image_types:
                return False, "Image type not allowed"
            if file_size > self.max_image_size:
                return False, "Image size exceeds maximum limit"
        elif mime_type not in self.allowed_file_types:
            return False, "File type not allowed"
        
        return True, "Valid file"

    # Generate unique filename based on timestamp and UUID
    async def generate_filename(self, original_filename: str) -> str:
        """Generate unique filename"""
        file_extension = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{unique_id}{file_extension}"

    async def save_file(self, file: UploadFile, subfolder: str = "files") -> Tuple[str, str, int]:
        """Save uploaded file and return filepath, filename, and size"""
        # Validate file
        is_valid, message = await self.validate_file(file)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        
        # Generate filename
        filename = self.generate_filename(file.filename)
        filepath = os.path.join(self.upload_dir, subfolder, filename)
        
        # Save file
        async with aiofiles.open(filepath, 'wb') as f:
            content = await file.read()
            await f.write(content)
            file_size = len(content)
        
        return filepath, filename, file_size

    async def create_thumbnail(self, image_path: str, size: Tuple[int, int] = (200, 200)) -> Optional[str]:
        """Create thumbnail for image"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Generate thumbnail filename
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                thumbnail_filename = f"{base_name}_thumb.jpg"
                thumbnail_path = os.path.join(self.upload_dir, "thumbnails", thumbnail_filename)
                
                # Save thumbnail
                img.save(thumbnail_path, "JPEG", quality=85)
                
                return thumbnail_path
        except Exception as e:
            print(f"Error creating thumbnail: {e}")
            return None

    async def get_image_dimensions(self, image_path: str) -> Tuple[Optional[int], Optional[int]]:
        """Get image dimensions"""
        try:
            with Image.open(image_path) as img:
                return img.width, img.height
        except Exception:
            return None, None

    async def get_file_hash(self, filepath: str) -> str:
        """Generate file hash for duplicate detection"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    async def delete_file(self, filepath: str) -> bool:
        """Delete file from filesystem"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

# Create global instance
file_handler = FileHandler()
