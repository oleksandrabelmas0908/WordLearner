import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey

from datetime import datetime 


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True, nullable=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(), nullable=False)


class Collection(Base):
    __tablename__ = "collections"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    words: Mapped[list["Word"]] = relationship(back_populates="collection")


class Word(Base):
    __tablename__ = "words"

    term: Mapped[str] = mapped_column(index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(), nullable=False)

    collection_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("collections.id"), nullable=False)

    definitions: Mapped[list["Definition"]] = relationship() 
    translations: Mapped[list["Translation"]] = relationship()


class Definition(Base):
    __tablename__ = "definitions"

    text: Mapped[str] = mapped_column(nullable=False)
    example: Mapped[str] = mapped_column(nullable=True)

    word_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("words.id"), nullable=False)


class Translation(Base):
    __tablename__ = "translations"

    language: Mapped[str] = mapped_column(String(20), nullable=False) # make a foraign key to languages table later
    text: Mapped[str] = mapped_column(nullable=False)

    word_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("words.id"), nullable=False)