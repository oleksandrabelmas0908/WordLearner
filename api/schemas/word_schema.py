from pydantic import BaseModel

from datetime import datetime
from uuid import UUID

from .definition_schema import DefinitionSchema, DefinitionAIOutputSchema
from .translation_schema import TranslationSchema


class WordCreateSchema(BaseModel):
    term: str
    collection_id: UUID


class WordSchema(WordCreateSchema):
    id: UUID
    created_at: datetime
    definitions: list["DefinitionSchema"] = []
    translations: list["TranslationSchema"] = []

    class Config:
        from_attributes = True


class WordAIOutputSchema(BaseModel):
    term: str
    definitions: list["DefinitionAIOutputSchema"] = []
    