from fastapi import APIRouter
from pynetbox_api.session import NetBoxBase

from pydantic import BaseModel, RootModel     
from typing import List

__all__ = [
    'TagsBasicSchema',
    'TagsSchema',
    'TagsSchemaList',
    'TagsSchemaIn',
    'Tags'
]

class TagsBasicSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display_url: str | None = None
    display: str | None = None
    name: str | None = None
    slug: str | None = None
    color: str | None = None
    
class TagsSchema(TagsBasicSchema):
    description: str | None = None
    object_type: list[str] | None = None
    tagged_items: int | None = None
    created: str | None = None
    last_updated: str | None = None
    
class TagsSchemaIn(BaseModel):
    name: str = 'Tag Placeholder'
    slug: str = 'tag-placeholder'
    color: str = '9e9e9e'
    description: str = 'Tag Placeholder Description'
    object_type: list[str] | None = None

TagsSchemaList = RootModel[List[TagsSchema]]

class Tags(NetBoxBase):
    app = 'extras'
    name = 'tags'
    schema = TagsSchema
    schema_in = TagsSchemaIn
    schema_list = TagsSchemaList
    unique_together = ['name', 'slug']
    
    # API 
    prefix = '/tags'
    api_router = APIRouter(tags=['Extras / Tags'])