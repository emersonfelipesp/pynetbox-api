from fastapi import APIRouter

from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase
from pynetbox_api.extras.tag import Tags

__all__ = [
    "ManufacturerSchema",
    "ManufacturerSchemaList",
    "ManufacturerSchemaIn",
    "Manufacturer"
]

class Manufacturer(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str | None = None
        name: str | None = None
        slug: str | None = None
        description: str | None = None
    
    class Schema(GenericSchema, BasicSchema):
        display_url: str | None = None

    class SchemaIn(BaseModel):
        name: str = 'Manufacturer Placeholder'
        slug: str = 'manufacturer-placeholder'
        description: str = 'Manufacturer Placeholder Description'
        tags: List[int] | None = None

    ManufacturerSchemaList = RootModel[List[Schema]]
    
    app = 'dcim'
    name = 'manufacturers'
    schema = Schema
    schema_in = SchemaIn
    schema_list = ManufacturerSchemaList
    unique_together = ['name', 'slug']
    
    # API
    prefix = '/manufacturer'
    api_router = APIRouter(tags=['DCIM / Manufacturer'])