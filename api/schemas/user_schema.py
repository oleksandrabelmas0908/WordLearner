from pydantic import BaseModel 

from datetime import datetime
from uuid import UUID


class UserCreateSchema(BaseModel):
    telegram_id: int | None = None
    username: str


class UserSchema(UserCreateSchema):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True