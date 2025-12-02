from pydantic import BaseModel

from .word_schema import WordSchema

from datetime import datetime


class CollectionCreateSchema(BaseModel):
    name: str
    description: str | None = None
    user_id: str


class CollectionSchema(CollectionCreateSchema):
    id: str
    created_at: datetime
    words: list["WordSchema"] = []

    class Config:
        orm_mode = True