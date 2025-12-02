from pydantic import BaseModel

from .word_schema import WordSchema

from datetime import datetime
from uuid import UUID


class CollectionCreateSchema(BaseModel):
    name: str
    description: str | None = None
    user_id: UUID


class CollectionSchema(CollectionCreateSchema):
    id: UUID
    created_at: datetime
    words: list["WordSchema"] = []

    class Config:
        from_attributes = True