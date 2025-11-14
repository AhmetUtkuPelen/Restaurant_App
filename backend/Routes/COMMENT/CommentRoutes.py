from fastapi import APIRouter, HTTPException, status
from Controllers.COMMENT.CommentControllers import CommentControllers
from Schemas.COMMENT.CommentSchemas import CommentCreate

CommentRouter = APIRouter(prefix="/comments", tags=["Comments"])