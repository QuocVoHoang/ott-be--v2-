from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User, ConversationParticipant, Conversation
from sqlalchemy.future import select
from database import get_db
from interface.interface import INewUserData, IUpdateUserAvatarData, IUpdateUserNameData
import datetime

user_router = APIRouter()

@user_router.get("/{user_id}")
async def get_user_by_id(user_id: str, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().all()
  return user

@user_router.get("/conversations/{user_id}")
async def get_user_conversations(user_id: str, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  
  result = await db.execute(
    select(ConversationParticipant.conversation_id)
    .where(ConversationParticipant.user_id == user_id)
  )
  conversation_ids = [row[0] for row in result.fetchall()]

  if not conversation_ids:
    return {"message": "User is not in any conversation", "conversations": []}
  
  result = await db.execute(
    select(Conversation).where(Conversation.id.in_(conversation_ids))
  )
  conversations = result.scalars().all()

  return conversations


@user_router.post("/")
async def create_new_user(data: INewUserData, db: AsyncSession = Depends(get_db)):
  existing_user = await db.execute(select(User).where(User.email == data.email))
  if existing_user is None:
    raise HTTPException(status_code=404, detail="Email already registered!")

  new_user = User(
    username=data.username,
    email=data.email,
    password=data.password
  )
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user


@user_router.put("/update-avatar/{user_id}")
async def update_user_avatar(user_id: str, data: IUpdateUserAvatarData, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().first()
  if user is None:
    raise HTTPException(status_code=404, detail="User not found")

  user.avatar_url = data.avatar_url
  user.updated_at = datetime.datetime.utcnow()
  
  await db.commit()
  await db.refresh(user)

  return {"message": "User avatar updated"}


@user_router.put("/update-username/{user_id}")
async def update_user_name(user_id: str, data: IUpdateUserNameData, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().first()
  if user is None:
    raise HTTPException(status_code=404, detail="User not found")

  user.username = data.username
  user.updated_at = datetime.datetime.utcnow()
  
  await db.commit()
  await db.refresh(user)

  return {"message": "User name updated"}


@user_router.delete("/{user_id}")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalars().first()
  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  await db.delete(user)
  await db.commit()

  return {"message": "User deleted successfully"}