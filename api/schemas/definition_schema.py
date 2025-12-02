from pydantic import BaseModel

from uuid import UUID


class DefinitionCreateSchema(BaseModel):
    text: str
    example: str | None = None
    word_id: UUID


class DefinitionSchema(DefinitionCreateSchema):
    id: UUID

    class Config:
        from_attributes = True