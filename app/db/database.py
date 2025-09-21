from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from typing import AsyncGenerator
import os

load_dotenv()
POSTGRES_CONN=os.environ.get("POSTGRES_CONN")
if POSTGRES_CONN is None:
    raise ValueError("POSTGRES_CONN is empty")
    
ASYNC_ENGINE=create_async_engine(POSTGRES_CONN)

ASYNC_SESSION_LOCAL = async_sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=ASYNC_ENGINE,
        class_=AsyncSession
        )
      
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with ASYNC_SESSION_LOCAL() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise Exception(f"Database error occurred: {e}")
        finally:
            await session.close()
    
