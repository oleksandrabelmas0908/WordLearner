from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager
import logging

from core.db import create_db_tables
from routes import user_router, collection_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield
    logger.info("Shutting down application...")
    

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(collection_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)