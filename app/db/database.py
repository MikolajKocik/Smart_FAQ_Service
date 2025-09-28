from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from typing import AsyncGenerator
import os

load_dotenv()
POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD")
POSTGRES_USER=os.environ.get("POSTGRES_USER")
POSTGRES_HOST=os.environ.get("POSTGRES_HOST")
POSTGRES_PORT=os.environ.get("POSTGRES_PORT")
POSTGRES_NAME=os.environ.get("POSTGRES_NAME")

if POSTGRES_PASSWORD is None:
    raise ValueError("POSTGRES_PASSWORD is missing")
    
POSTGRES_CONN=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

ASYNC_ENGINE=create_async_engine(POSTGRES_CONN)

ASYNC_SESSION_LOCAL = async_sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=ASYNC_ENGINE,
        class_=AsyncSession
        )
      
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with ASYNC_SESSION_LOCAL() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise Exception(f"Database error occurred: {e}")
        finally:
            await session.close()
    
