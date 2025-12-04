from fastapi import APIRouter, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool

from uuid import UUID

from schemas import WordCreateSchema, WordSchema
from core.db import get_session
from services.agents import process_word


router = APIRouter(prefix="/words", tags=["words"])


@router.post("/")
async def create_word(
    word_create: WordCreateSchema,
    session=Depends(get_session),
):
    res = process_word(word_create.term)
    return {"detail": res}
