# from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
# from message.message_service import websocket_manager
# from sqlalchemy.ext.asyncio import AsyncSession
# from models.models import User
# from sqlalchemy.future import select
# from database import get_db

# message_router = APIRouter()

# @message_router.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: str):
#   await websocket_manager.connect(websocket, user_id)
#   try:
#     while True:
#       data = await websocket.receive_json()
      
#       if "conversation_id" not in data or "content" not in data:
#         await websocket.send_json({"error": "Invalid message format"})
#         continue

#       conversation_id = data["conversation_id"]
#       content = data["content"]

#       conversation = await conversation_collection.find_one({"_id": ObjectId(conversation_id)})
#       if not conversation:
#         await websocket.send_json({"error": "Conversation not found"})
#         continue

#       if user_id not in conversation["participants"]:
#         await websocket.send_json({"error": "Sender is not in this conversation"})
#         continue

#       message_data = {
#         "conversation_id": conversation_id,
#         "sender": user_id,
#         "content": content,
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow(),
#         "type": "text"
#       }

#       result = await message_collection.insert_one(message_data)
#       message_data["_id"] = str(result.inserted_id)
#       await websocket_manager.broadcast(message_data, conversation_id)
#   except WebSocketDisconnect:
#     websocket_manager.disconnect(websocket, user_id)