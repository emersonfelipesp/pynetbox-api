from pynetbox_api.session import NetBoxBase

from pydantic import BaseModel, RootModel, AnyHttpUrl  
from typing import List, Optional, Union

from pynetbox_api.utils import GenericSchema, ValueLabelSchema
from pynetbox_api.dcim.interface import Interface, InterfaceBasicSchema
from pynetbox_api.extras import Tags, TagsSchema

__all__ = [
    'IPAddressBasicSchema',
    'IPAddressSchema',
    'IPAddressSchemaList',
    'IPAddressSchemaIn',
    'IPAddress'
]

class IPAddressBasicSchema(BaseModel):
    id: int | None = None
    url: AnyHttpUrl | None = None
    display: str  | None = None
    address: str | None = None
    description: str | None = None
    
class IPAddressSchema(IPAddressBasicSchema, GenericSchema):
    display_url: AnyHttpUrl | None = None
    family: ValueLabelSchema | None = None
    vrf: Optional[Union[str, None]] = None
    tenant: Optional[Union[str, None]] = None
    status: ValueLabelSchema | None = None
    role: Optional[Union[str, None]] = None
    assigned_object_type: str | None = None
    assigned_object_id: int | None = None
    assigned_object: Optional[Union[str, InterfaceBasicSchema]] = None
    nat_inside: Optional[Union[str, None]] = None
    nat_outside: List = []
    dns_name: str | None = None
    comments: str | None = None

class IPAddressSchemaIn(BaseModel):
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
    assgined_object: Optional[Union[str, InterfaceBasicSchema]] = None
    nat_inside: Optional[Union[str, None]] = None
    comments: str | None = None

IPAddressSchemaList = RootModel[List[IPAddressSchema]]

class IPAddress(NetBoxBase):
    app = 'ipam'
    name = 'ip_addresses'
    schema = IPAddressSchema
    schema_in = IPAddressSchemaIn
    schema_list = IPAddressSchemaList
    unique_together = ['address']
    required_fields = ['address', 'status']
    

