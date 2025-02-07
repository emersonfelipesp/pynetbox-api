from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.schemas.extras import TagsSchema, TagsSchemaIn

__all__ = [
    'DeviceRoleSchema',
    'DeviceRoleSchemaList',
    'DeviceRoleSchemaIn'
]

class DeviceRoleSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display_url: str | None = None
    display: str | None = None
    name: str | None = None
    slug: str | None = None
    vm_role: bool | None = None
    config_template: str | None = None
    description: str | None = None
    tags: List[TagsSchema] | None = None
    custom_fields: dict[str, str | None] = {}
    created: str | None = None
    last_updated: str | None = None
    device_count: int | None = None
    virtualmachine_count: int | None = None
    
class DeviceRoleSchemaIn(BaseModel):
    name: str = 'Device Role Placeholder'
    slug: str = 'device-role-placeholder'
    color: str = '9e9e9e'
    vm_role: bool = True
    config_template: str | None = None
    description: str = 'Placeholder object for ease data ingestion'
    tags: List[int]
    
DeviceRoleSchemaList = RootModel[List[DeviceRoleSchema]]