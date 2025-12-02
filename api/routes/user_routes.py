from fastapi import APIRouter, Depends

from schemas import UserCreateSchema, UserSchema
from core.db import get_session
from services.crud.user_crud import create_user_db


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserSchema)
async def create_user(
    user_create: UserCreateSchema,
    session=Depends(get_session),
) -> UserSchema:
    
    user = await create_user_db(session, user_create)
    return user


