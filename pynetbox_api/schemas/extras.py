from pydantic import BaseModel, RootModel     
from typing import List

__all__ = [
    'TagsSchema',
    'TagsSchemaList',
    'TagsSchemaIn'
]

class TagsSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display_url: str | None = None
    display: str | None = None
    name: str | None = None
    slug: str | None = None
    color: str | None = None
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