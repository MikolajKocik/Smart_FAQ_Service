from contextlib import asynccontextmanager
from app.db.schemas.common.Base import Base
from app.db.database import ASYNC_ENGINE, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from agent.ai_agent import ask_faq_agent
from app.dtos.ask_request_dto import AskRequest
from app.dtos.ask_response_dto import AskResponse
from app.dtos.faq_create_dto import FaqCreate
from app.dtos.faq_read_dto import FaqRead
from app.services.faq_service import FaqService
from app.repositories.faq_repository import FaqRepository
import uvicorn
from typing import List, Optional
from fastapi import (
    FastAPI, 
    HTTPException,
    Depends,
    status
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ASYNC_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.state.db_engine = ASYNC_ENGINE
    yield

    await app.state.db_engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.post("/ask", status_code=status.HTTP_200_OK, 
        responses= {
            status.HTTP_400_BAD_REQUEST: {"description": "Invalid question"},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
        }
)
async def ask(
    user_question: AskRequest,
    session: AsyncSession = Depends(get_session)):
    if not user_question.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty"
        )

    try:
        result: AskResponse = await ask_faq_agent(session, user_question.question) 

        return AskResponse(answer=result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ocurred while processing some action: {str(e)}")

@app.post("/faqs/create", response_model= FaqCreate, status_code=status.HTTP_201_CREATED)
async def add_faq(
        faq: FaqCreate,
        session: AsyncSession = Depends(get_session)          
) -> FaqCreate:    
    try:
        service = FaqService(FaqRepository(session))
        result = await service.create_faq(faq)
        return result
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )


@app.get("/faqs/{id}", response_model=FaqRead, status_code=status.HTTP_200_OK)
async def get_faq(faq_id: int, session: AsyncSession = Depends(get_session)) -> FaqRead:
    if faq_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    try:
       service = FaqService(FaqRepository(session))
       faq = await service.get_faq(faq_id)
       return faq
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )
    

@app.get("/faqs", status_code=status.HTTP_200_OK)
async def get_faqs(session: AsyncSession = Depends(get_session)) -> Optional[List[FaqRead]]:
    service = FaqService(FaqRepository(session))
    faqs = await service.get_faqs()
    return faqs

@app.put("/faqs/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_faq(
    id: int,
    session: AsyncSession = Depends(get_session)
) -> None:
    service = FaqService(FaqRepository(session))
    faq = await service.get_faq(id)
    if not faq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    try:
        await service.faq_update(faq)
        return None
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )

@app.delete("/faqs/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_faq(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    try:  
        service = FaqService(FaqRepository(session))
        await service.faq_remove(id)
        return None
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={str(e)}
        )


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
