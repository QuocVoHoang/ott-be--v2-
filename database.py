# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # DB_URL =  os.getenv("DATABASE_URL")

# # Tạo engine kết nối database
# engine = create_async_engine(DB_URL, echo=True, future=True)

# # Tạo session factory
# AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# # Hàm để lấy session trong route của FastAPI
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session
