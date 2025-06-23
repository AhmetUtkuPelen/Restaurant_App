from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import magic
from Services.FileUpload import file_handler
from Models.database_models import AttachmentDB
from Models.Message.MessageModel import AttachmentType
from database import get_db

router = APIRouter(prefix="/files", tags=["files"])

def get_attachment_type(mime_type: str) -> AttachmentType:
    """Determine attachment type from MIME type"""
    if mime_type.startswith('image/'):
        return AttachmentType.IMAGE
    elif mime_type.startswith('video/'):
        return AttachmentType.VIDEO
    elif mime_type.startswith('audio/'):
        return AttachmentType.AUDIO
    else:
        return AttachmentType.DOCUMENT

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a file for chat messages"""
    try:
        # Determine subfolder based on file type
        content = await file.read()
        await file.seek(0)
        mime_type = magic.from_buffer(content, mime=True)
        
        subfolder = "images" if mime_type.startswith('image/') else "files"
        
        # Save file
        filepath, filename, file_size = await file_handler.save_file(file, subfolder)
        
        # Create thumbnail for images
        thumbnail_path = None
        width, height = None, None
        if mime_type.startswith('image/'):
            thumbnail_path = await file_handler.create_thumbnail(filepath)
            width, height = file_handler.get_image_dimensions(filepath)
        
        # Create attachment record (without message_id for now)
        attachment = AttachmentDB(
            filename=filename,
            original_filename=file.filename,
            file_size=file_size,
            mime_type=mime_type,
            attachment_type=get_attachment_type(mime_type),
            url=f"/files/download/{filename}",
            thumbnail_url=f"/files/thumbnail/{os.path.basename(thumbnail_path)}" if thumbnail_path else None,
            width=width,
            height=height,
            message_id="temp"  # Will be updated when message is created
        )
        
        db.add(attachment)
        db.commit()
        db.refresh(attachment)
        
        return {
            "id": attachment.id,
            "filename": filename,
            "original_filename": file.filename,
            "file_size": file_size,
            "mime_type": mime_type,
            "attachment_type": attachment.attachment_type,
            "url": attachment.url,
            "thumbnail_url": attachment.thumbnail_url,
            "width": width,
            "height": height
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download a file"""
    # Check in both images and files directories
    for subfolder in ["images", "files"]:
        filepath = os.path.join(file_handler.upload_dir, subfolder, filename)
        if os.path.exists(filepath):
            return FileResponse(
                filepath,
                filename=filename,
                media_type='application/octet-stream'
            )
    
    raise HTTPException(status_code=404, detail="File not found")

@router.get("/thumbnail/{filename}")
async def get_thumbnail(filename: str):
    """Get thumbnail for an image"""
    filepath = os.path.join(file_handler.upload_dir, "thumbnails", filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type='image/jpeg')
    
    raise HTTPException(status_code=404, detail="Thumbnail not found")

@router.delete("/delete/{attachment_id}")
async def delete_file(attachment_id: str, db: Session = Depends(get_db)):
    """Delete a file and its attachment record"""
    attachment = db.query(AttachmentDB).filter(AttachmentDB.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    # Delete file from filesystem
    for subfolder in ["images", "files"]:
        filepath = os.path.join(file_handler.upload_dir, subfolder, attachment.filename)
        if os.path.exists(filepath):
            file_handler.delete_file(filepath)
            break
    
    # Delete thumbnail if exists
    if attachment.thumbnail_url:
        thumbnail_filename = os.path.basename(attachment.thumbnail_url)
        thumbnail_path = os.path.join(file_handler.upload_dir, "thumbnails", thumbnail_filename)
        file_handler.delete_file(thumbnail_path)
    
    # Delete attachment record
    db.delete(attachment)
    db.commit()
    
    return {"message": "File deleted successfully"}
