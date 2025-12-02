from pydantic import BaseModel

from uuid import UUID


class TranslationCreateSchema(BaseModel):
    language: str
    text: str
    word_id: UUID

class TranslationSchema(TranslationCreateSchema):
    id: UUID

    class Config:
        from_attributes = True