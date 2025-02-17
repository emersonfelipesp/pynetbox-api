from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List, Any, Optional, Union

from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase
from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.extras.tag import Tags

class Platform(NetBoxBase):
    class BasicSchema(NetBoxBase.BasicSchema):
        pass
    
    class Schema(GenericSchema, BasicSchema):
        manufacturer: Manufacturer.BasicSchema | None = None
        config_template: Optional[Union[Any, None]] = None # TODO: Fix this
        device_count: int | None = None
        virtual_machine_count: int | None = None
    
    class SchemaIn(BaseModel):
        name: str = 'Placeholder Platform'
        slug: str = 'placeholder-platform'
        manufacturer: int | None = None
        config_template: Optional[Union[Any, None]] = None
        description: None = None
        tags: List[int] | None = None

    SchemaList = RootModel[List[Schema]]
    
    # NetBox API Endpoint: /dcim/platforms/
    app: str = 'dcim'
    name: str = 'platforms'
    
    # Schema for Platform objects
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    
    # Unique constraints for Platform objects
    unique_together = ['name', 'slug']
    required_fields = ['name', 'slug']
    
    # API
    prefix = '/platform'
    api_router = APIRouter(tags=['DCIM / Platform'])
    