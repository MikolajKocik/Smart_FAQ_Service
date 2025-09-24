from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi import Depends, status
from .db.schemas.common.Base import Base
from .db.database import ASYNC_ENGINE, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..agent.ai_agent import ask_faq_agent
from .dtos.ask_request_dto import AskRequest
from .dtos.ask_response_dto import AskResponse
import uvicorn

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

        return Response(
            content=result.answer,
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ocurred while processing some action: {str(e)}")

@app.post("/faq")
async def faq():
    pass

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
