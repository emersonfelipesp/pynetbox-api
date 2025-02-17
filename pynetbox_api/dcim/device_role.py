from fastapi import APIRouter
from pynetbox_api.session import NetBoxBase

from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.extras.tag import Tags

__all__ = [
    'DeviceRole'
]

class DeviceRole(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str | None = None
        name: str | None = None
        slug: str | None = None
        description: str | None = None 
            
    class Schema(BasicSchema):
        display_url: str | None = None
        vm_role: bool | None = None
        config_template: str | None = None
        tags: List[Tags.Schema] | None = None
        custom_fields: dict[str, str | None] = {}
        created: str | None = None
        last_updated: str | None = None
        device_count: int | None = None
        virtualmachine_count: int | None = None
        
    class SchemaIn(BaseModel):
        name: str = 'Device Role Placeholder'
        slug: str = 'device-role-placeholder'
        color: str = '9e9e9e'
        vm_role: bool = True
        config_template: str | None = None
        description: str = 'Placeholder object for ease data ingestion'
        tags: List[int]
        
    SchemaList = RootModel[List[Schema]]
    
    app = 'dcim'
    name = 'device_roles'
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    unique_together = ['name', 'slug']
    
    # API
    prefix = '/device_role'
    api_router = APIRouter(tags=['DCIM / Device Role'])
