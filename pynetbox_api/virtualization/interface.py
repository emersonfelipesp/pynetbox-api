from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List
from pynetbox_api.virtualization.virtual_machine import VirtualMachine
from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase

__all__ = [
    'VMInterfaceBasicSchema',
    'VMInterfaceSchema',
    'VMInterfaceSchemaList',
    'VMInterfaceSchemaIn',
    'VMInterface'
]


class VMInterfaceBasicSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display: str  | None = None
    name: str | None = None
    description: str | None = None


class VMInterfaceSchema(GenericSchema, VMInterfaceBasicSchema):
    virtual_machine: VirtualMachine.BasicSchema | None = None
    enabled: bool | None = None
    parent: VMInterfaceBasicSchema | None = None
    bridge: VMInterfaceBasicSchema | None = None
    mtu: int | None = None  
    mac_address: str | None = None
    primary_mac_address: str | None = None
    mac_addresses: List[str] | None = None
    mode: str | None = None
    untagged_vlan: str | None = None
    tagged_vlans: List[str] | None = None
    qinq_svlan: str | None = None
    vlan_translation_policy: str | None = None
    vrf: str | None = None
    l2vpn_translation_policy: str | None = None
    count_ipaddresses: int | None = None
    count_fhrp_groups: int | None = None


class VMInterfaceSchemaIn(BaseModel):
    virtual_machine: int = VirtualMachine(bootstrap_placeholder=True).get('id', 0)
    name: str = 'Virtual Machine Interface Placeholder'
    enabled: bool = True
    description: str | None = None
    tags: List[int] = []
    vrf: str | None = None
    primary_mac_address: str | None = None # MACAddress
    mtu: int | None = None
    parent: int | None = None # VMInterfaceBasicSchema
    bridge: int | None = None # VMInterfaceBasicSchema
    mode: str | None = None
    vlan_translation_policy: str | None = None
    

VMInterfaceSchemaList = RootModel[List[VMInterfaceSchema]]

class VMInterface(NetBoxBase):
    # NetBox API endpoint: /api/virtualization
    app: str = 'virtualization'
    name: str = 'interfaces'
    schema = VMInterfaceSchema
    schema_in = VMInterfaceSchemaIn
    schema_list = VMInterfaceSchemaList
    
    # Unique constraints for VMInterface objects
    unique_together = ['name', 'virtual_machine']
    required_fields = ['name', 'virtual_machine']
    
    # API
    prefix = '/interface'
    api_router = APIRouter(tags=['Virtualization / Interface'])