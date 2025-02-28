from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List
from pynetbox_api.virtualization.virtual_machine import VirtualMachine
from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase

__all__ = [
    'VirtualDisk'
]

class VirtualDisk(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str  | None = None
        name: str | None = None
        description: str | None = None

    class Schema(GenericSchema, BasicSchema):
        display_url: str | None = None
        virtual_machine: VirtualMachine.BasicSchema | None = None
        size: int

    class SchemaIn(BaseModel):
        virtual_machine: int = VirtualMachine(bootstrap_placeholder=True).get('id')
        name: str = 'Virtual Disk Placeholder'
        size: int = 1
        description: str | None = None
        tags: List[int] = []

    SchemaList = RootModel[List[Schema]]

    app: str = 'virtualization'
    name: str = 'virtual_disks'
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    unique_together = ['name', 'virtual_machine']
    required_fields = ['name', 'virtual_machine']
    
    # API
    prefix = '/virtual_disk'
    api_router = APIRouter(tags=['Virtualization / Virtual Disk'])
