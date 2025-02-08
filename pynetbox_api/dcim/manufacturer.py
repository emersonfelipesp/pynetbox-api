from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.session import NetBoxBase
from pynetbox_api.extras import TagsSchema

__all__ = [
    "ManufacturerSchema",
    "ManufacturerSchemaList",
    "ManufacturerSchemaIn",
    "Manufacturer"
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
    custom_fields: dict[str, str | None] = {}
    created: str | None = None
    last_updated: str | None = None

class ManufacturerSchemaIn(BaseModel):
    name: str = 'Manufacturer Placeholder'
    slug: str = 'manufacturer-placeholder'
    description: str = 'Manufacturer Placeholder Description'
    tags: List[int] | None = None

ManufacturerSchemaList = RootModel[List[ManufacturerSchema]]

class Manufacturer(NetBoxBase):
    app = 'dcim'
    name = 'manufacturers'
    schema = ManufacturerSchema
    schema_in = ManufacturerSchemaIn
    schema_list = ManufacturerSchemaList
    unique_together = ['name', 'slug']