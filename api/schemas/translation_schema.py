from pydantic import BaseModel


class TranslationCreateSchema(BaseModel):
    language: str
    text: str
    word_id: str

class TranslationSchema(TranslationCreateSchema):
    id: str

    class Config:
        orm_mode = True