from core.db import User 
from schemas import UserCreateSchema, UserSchema

from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_db(session: AsyncSession, user_create: UserCreateSchema) -> UserSchema:
    try:        
        user = User(telegram_id=user_create.telegram_id, username=user_create.username)     
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return UserSchema.model_validate(user)
    
    except Exception as e:
        await session.rollback()
        raise e
    