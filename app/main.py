from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db.schemas.common.Base import Base
from .db.database import ASYNC_ENGINE
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ASYNC_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.state.db_engine = ASYNC_ENGINE
    yield

    await app.state.db_engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.post("/ask")
async def ask():
    pass

@app.post("/faq")
async def faq():
    pass

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
