from core.db import Collection, Word
from schemas import CollectionCreateSchema, CollectionSchema

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


async def create_collection_db(session: AsyncSession, collection_create: CollectionCreateSchema) -> CollectionSchema:
    try:        
        collection = Collection(
            name=collection_create.name,
            description=collection_create.description,
            user_id=collection_create.user_id
        )     
        session.add(collection)
        await session.commit()
        
        # Reload with relationships eagerly loaded (including nested)
        result = await session.execute(
            select(Collection)
            .options(
                selectinload(Collection.words)
                .selectinload(Word.definitions),
                selectinload(Collection.words)
                .selectinload(Word.translations),
            )
            .where(Collection.id == collection.id)
        )
        collection = result.scalar_one()

        return CollectionSchema.model_validate(collection)
    
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e.orig)
        if "ix_collections_name" in error_message or "collections_name_key" in error_message:
            raise HTTPException(status_code=400, detail="Collection with this name already exists.")
        elif "collections_user_id_fkey" in error_message or "ForeignKeyViolation" in error_message:
            raise HTTPException(status_code=404, detail="User not found.")
        else:
            raise HTTPException(status_code=400, detail="Database integrity error.")
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

async def get_collections_by_user_db(session: AsyncSession, user_id: UUID) -> list[CollectionSchema]:
    try:
        result = await session.execute(
            select(Collection)
            .options(
                selectinload(Collection.words)
                .selectinload(Word.definitions),
                selectinload(Collection.words)
                .selectinload(Word.translations),
            )
            .where(Collection.user_id == user_id)
        )
        db_collections = result.scalars().all()

        collections = [CollectionSchema.model_validate(collection) for collection in db_collections]
        return collections
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def delete_collection_db(session: AsyncSession, collection_id: UUID):
    try:
        result = await session.execute(
            select(Collection).where(Collection.id == collection_id)
        )
        collection = result.scalar_one_or_none()

        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found.")

        await session.delete(collection)
        await session.commit()
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))