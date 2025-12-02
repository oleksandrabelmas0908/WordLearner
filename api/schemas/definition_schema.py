from pydantic import BaseModel


class DefinitionCreateSchema(BaseModel):
    text: str
    example: str | None = None
    word_id: str


class DefinitionSchema(DefinitionCreateSchema):
    id: str

    class Config:
        orm_mode = True