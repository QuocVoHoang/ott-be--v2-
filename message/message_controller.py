from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from sqlalchemy.future import select
from database import get_db

message_router = APIRouter()

@message_router.get("/health")
async def read_root():
    return {"message": "BACKEND RUNNING"}