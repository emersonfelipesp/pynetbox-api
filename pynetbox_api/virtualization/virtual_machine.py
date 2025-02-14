from fastapi import APIRouter
from pydantic import BaseModel, RootModel, AnyHttpUrl
from typing import List, Optional, Union
from pynetbox_api.utils import GenericSchema, ValueLabelSchema
from pynetbox_api.virtualization.cluster import Cluster, ClusterBasicSchema
from pynetbox_api.dcim.site import SiteBasicSchema
from pynetbox_api.dcim.device import DeviceBasicSchema
from pynetbox_api.dcim.device_role import DeviceRoleBasicSchema as RoleBasicSchema
from pynetbox_api.ipam.ip_address import IPAddressBasicSchema
from pynetbox_api.session import NetBoxBase

__all__ = [
    'VirtualMachineBasicSchema',
    'VirtualMachineSchema',
    'VirtualMachineSchemaList',
    'VirtualMachineSchemaIn',
    'VirtualMachine'
]

class VirtualMachineBasicSchema(BaseModel):
    id: int | None = None
    url: AnyHttpUrl | None = None
    display: str  | None = None
    name: str | None = None
    description: str | None = None


class VirtualMachineSchema(GenericSchema, VirtualMachineBasicSchema):
    display_url: AnyHttpUrl | None = None
    status: ValueLabelSchema | None = None
    site: SiteBasicSchema | None = None
    cluster: ClusterBasicSchema | None = None
    device: DeviceBasicSchema | None = None
    serial: str | None = None
    role: RoleBasicSchema | None = None
    tenant: str | None = None # TenantBasicSchema
    platform: str | None = None
    primary_ip: IPAddressBasicSchema | None = None
    primary_ip4: IPAddressBasicSchema | None = None
    primary_ip6: IPAddressBasicSchema | None = None
    vcpus: Optional[Union[int, float]] = None
    memory: Optional[Union[int, float]] = None
    disk: Optional[Union[int, float]] = None
    config_template: str | None = None
    local_context_data: dict[str, str | None] = {}
    config_context: dict[str, str | None] = {}
    interface_count: int | None = None
    virtual_disk_count: int | None = None


class VirtualMachineSchemaIn(BaseModel):
    name: str = 'Virtual Machine Placeholder'
    role: str | None = None
    status: str = 'active'
    description: str | None = None
    serial: str | None = None
    tags: List[int] = []
    site: int | None = None
    cluster: int = Cluster(bootstrap_placeholder=True).id
    device: int | None = None
    tenant_group: str | None = None
    tenant: str | None = None
    platform: str | None = None
    primary_ip: int | None = None
    primary_ip4: int | None = None
    primary_ip6: int | None = None
    config_template: int | None = None
    vcpus: Optional[Union[int, float]] = None
    memory: Optional[Union[int, float]] = None
    disk: Optional[Union[int, float]] = None
    config_context: str | None = None


VirtualMachineSchemaList = RootModel[List[VirtualMachineSchema]]


class VirtualMachine(NetBoxBase):
    # NetBox API endpoint: /virtualization/virtual-machines/
    app: str = 'virtualization'
    name: str = 'virtual_machines'
    
    # Schema for VirtualMachine objects
    schema = VirtualMachineSchema
    schema_in = VirtualMachineSchemaIn
    schema_list = VirtualMachineSchemaList
    
    # Unique constraints for VirtualMachine objects
    unique_together = ['name']
    required_fields = ['name', 'status']

    # API
    prefix = '/virtual_machine'
    api_router = APIRouter(tags=['Virtualization / Virtual Machine'])
    