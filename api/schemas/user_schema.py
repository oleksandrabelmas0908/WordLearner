from pydantic import BaseModel 

from datetime import datetime


class UserCreateSchema(BaseModel):
    telegram_id: int | None = None
    username: str


class UserSchema(UserCreateSchema):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True