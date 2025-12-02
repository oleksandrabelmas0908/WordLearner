from fastapi import APIRouter, Depends

from uuid import UUID

from schemas import CollectionCreateSchema, CollectionSchema
from core.db import get_session
from services.crud.collaction_crud import create_collection_db, get_collections_by_user_db, delete_collection_db


router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("/", response_model=CollectionSchema)
async def create_collection(
    collection_create: CollectionCreateSchema,
    session=Depends(get_session),
) -> CollectionSchema:
    
    collection = await create_collection_db(session, collection_create)
    return collection


@router.get("/collections/{user_id}", response_model=list[CollectionSchema])
async def get_collections(
    user_id: UUID,
    session=Depends(get_session),
) -> list[CollectionSchema]:
    
    collections = await get_collections_by_user_db(session, user_id)
    return collections


@router.delete("/{collection_id}")
async def delete_collection(
    collection_id: UUID,
    session=Depends(get_session),
):
    await delete_collection_db(session, collection_id)
    return {"detail": "Collection deleted successfully."}
