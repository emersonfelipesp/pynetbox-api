from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.schemas.extras import TagsSchema

__all__ = [
    "ManufacturerSchema",
    "ManufacturerSchemaList",
    "ManufacturerSchemaIn"
]

class ManufacturerSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display: str | None = None
    display_url: str | None = None
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    tags: List[TagsSchema] | None = None
    custom_fields: dict | None = None
    created: str | None = None
    last_updated: str | None = None

class ManufacturerSchemaIn(BaseModel):
    name: str
    slug: str
    description: str | None = None
    tags: List[int] | None = None

ManufacturerSchemaList = RootModel[List[ManufacturerSchema]]