from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.extras import Tags
from pynetbox_api.schemas.extras import (
    TagsSchema,
    TagsSchemaIn,
    TagsSchemaList
)

extras_router = APIRouter(tags=['Extras / Tags'])

@extras_router.get('/tags', response_model=TagsSchemaList)
async def get_tags() -> TagsSchemaList:
    return Tags().all()

@extras_router.get('/tags/{tag_id}')
async def get_tag(tag_id: int) -> TagsSchema:
    return Tags().get(id=tag_id)

@extras_router.post('/tags')
async def create_tag(tag: TagsSchemaIn) -> TagsSchema:
    return Tags(**tag.model_dump(exclude_unset=True))

@extras_router.post('/tags/placeholder')
async def create_tag_placeholder(use_placeholder: Annotated[bool | None, Query()] = True) -> TagsSchema:
    return Tags(use_placeholder=use_placeholder)

@extras_router.put('/tags/{tag_id}')
async def update_tag(tag_id: int, tag: TagsSchema) -> JSONResponse:
    return Tags().update(id=tag_id, json=tag.model_dump(exclude_unset=True))

@extras_router.delete('/tags/{tag_id}')
async def delete_tag(tag_id: int) -> JSONResponse:
    return Tags().delete(id=tag_id)