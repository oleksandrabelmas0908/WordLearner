from pydantic import BaseModel

from datetime import datetime

from .definition_schema import DefinitionSchema
from .translation_schema import TranslationSchema


class WordCreateSchema(BaseModel):
    term: str
    collection_id: str


class WordSchema(WordCreateSchema):
    id: str
    created_at: datetime
    definitions: list["DefinitionSchema"] = []
    translations: list["TranslationSchema"] = []

    class Config:
        orm_mode = True