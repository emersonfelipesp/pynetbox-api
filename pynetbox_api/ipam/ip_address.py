from pynetbox_api.session import NetBoxBase

from pydantic import BaseModel, RootModel, AnyHttpUrl  
from typing import List, Optional, Union
from pynetbox_api.utils import GenericSchema
from pynetbox_api.dcim.interface import Interface

__all__ = [
    'IPAddress'
]
class Family(BaseModel):
    value: int | None = None
    label: str | None = None
        
class IPAddress(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: AnyHttpUrl | None = None
        display: str  | None = None
        address: str | None = None
        description: str | None = None
        
    class Schema(BasicSchema, GenericSchema):
        display_url: AnyHttpUrl | None = None
        family: Family | None = None
        vrf: Optional[Union[str, None]] = None
        tenant: Optional[Union[str, None]] = None
        status: NetBoxBase.ValueLabelSchema | None = None
        role: Optional[Union[str, None]] = None
        assigned_object_type: str | None = None
        assigned_object_id: int | None = None
        assigned_object: Optional[Union[str, Interface.BasicSchema]] = None
        nat_inside: Optional[Union[str, None]] = None
        nat_outside: List = []
        dns_name: str | None = None
        comments: str | None = None

    class SchemaIn(BaseModel):
        address: str = '127.0.0.1/24'
        status: str = 'active'
        role: str | None = None
        vrf: str | None = None
        dns_name: str | None = None
        description: str | None = None
        tags: List[int] = []
        tenant_group: str | None = None
        tenant: str | None = None
        assigned_object_type: str | None = None
        assigned_object_id: int | None = None
        assgined_object: Optional[Union[str, Interface.BasicSchema]] = None
        nat_inside: Optional[Union[str, None]] = None
        comments: str | None = None

    SchemaList = RootModel[List[Schema]]
    
    app = 'ipam'
    name = 'ip_addresses'
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    unique_together = ['address']
    required_fields = ['address', 'status']
    

