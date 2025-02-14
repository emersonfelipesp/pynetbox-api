from fastapi import APIRouter
from pydantic import BaseModel, RootModel, AnyHttpUrl
from typing import List
from pynetbox_api.virtualization.virtual_machine import VirtualMachine, VirtualMachineBasicSchema
from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase

__all__ = [
    'VirtualDiskBasicSchema',
    'VirtualDiskSchema',
    'VirtualDiskSchemaList',
    'VirtualDiskSchemaIn',
    'VirtualDisk'
]

class VirtualDiskBasicSchema(BaseModel):
    id: int | None = None
    url: AnyHttpUrl | None = None
    display: str  | None = None
    name: str | None = None
    description: str | None = None

class VirtualDiskSchema(GenericSchema, VirtualDiskBasicSchema):
    display_url: AnyHttpUrl | None = None
    virtual_machine: VirtualMachineBasicSchema | None = None
    size: int

class VirtualDiskSchemaIn(BaseModel):
    virtual_machine: int = VirtualMachine(bootstrap_placeholder=True).id
    name: str = 'Virtual Disk Placeholder'
    size: int = 1
    description: str | None = None
    tags: List[int] = []

VirtualDiskSchemaList = RootModel[List[VirtualDiskSchema]]

class VirtualDisk(NetBoxBase):
    app: str = 'virtualization'
    name: str = 'virtual_disks'
    schema = VirtualDiskSchema
    schema_in = VirtualDiskSchemaIn
    schema_list = VirtualDiskSchemaList
    unique_together = ['name', 'virtual_machine']
    required_fields = ['name', 'virtual_machine']
    
    # API
    prefix = '/virtual_disk'
    api_router = APIRouter(tags=['Virtualization / Virtual Disk'])
