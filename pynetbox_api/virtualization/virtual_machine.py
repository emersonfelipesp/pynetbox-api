from fastapi import APIRouter
from pydantic import BaseModel, RootModel, Field
from typing import List, Optional, Union
from pynetbox_api.utils import GenericSchema
from pynetbox_api.virtualization.cluster import Cluster
from pynetbox_api.dcim.site import Site
from pynetbox_api.dcim.device_role import DeviceRole as Role
from pynetbox_api.session import NetBoxBase
from pynetbox_api.ipam.ip_address import IPAddress
from pynetbox_api.dcim.device import Device
from pynetbox_api.dcim.platform import Platform
from pynetbox_api.extras.tag import Tags
from pynetbox_api.exceptions import FastAPIException

__all__ = [
    'VirtualMachine',
]

from enum import Enum


class VirtualMachine(NetBoxBase):
    def _bootstrap_placeholder(self) -> dict:
        """
        Override to use instance-specific nb (netbox session) parameter for placeholder creation
        The default placeholder creation uses the default nb parameter (class level)
        """
        try:
            # Create a custom SchemaIn instance with the instance's nb parameter
            tags_obj = Tags(bootstrap_placeholder=True, nb=self.nb)
            role_obj = Role(bootstrap_placeholder=True, nb=self.nb)
            cluster_obj = Cluster(bootstrap_placeholder=True, nb=self.nb)
            
            return self.schema_in(
                tags=[tags_obj.id if tags_obj.id is not None else 0],
                role=role_obj.id if role_obj.id is not None else 0,
                cluster=cluster_obj.id if cluster_obj.id is not None else 0
            ).model_dump(exclude_none=True)
        
        except Exception as error:
            raise FastAPIException(
                message=f'Error to create placeholder object {self.app}.{self.name}',
                python_exception=str(error)
            )
            
    class StatusField(Enum):
        """
        Key are Netbox Status.
        Values are Proxmox Status.
        """
        active = "online"
        #active = "running"
        offline = "stopped"
        prelaunch = "prelaunch"
    
    status_field: dict = {
        'online': 'active',
        'running': 'active',
        'stopped': 'offline',
        'prelaunch': 'prelaunch',
    }

    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str  | None = None
        name: str | None = None
        description: str | None = None


    class Schema(GenericSchema, BasicSchema):
        display_url: str | None = None
        status: NetBoxBase.ValueLabelSchema | None = None
        site: Site.BasicSchema | None = None
        cluster: Cluster.BasicSchema | None = None
        device: Device.BasicSchema | None = None
        serial: str | None = None
        role: Role.BasicSchema | None = None
        tenant: str | None = None # TenantBasicSchema
        platform: Platform.BasicSchema | None = None
        primary_ip: IPAddress.BasicSchema | None = None
        primary_ip4: IPAddress.BasicSchema | None = None
        primary_ip6: IPAddress.BasicSchema | None = None
        vcpus: Optional[Union[int, float]] = None
        memory: Optional[Union[int, float]] = None
        disk: Optional[Union[int, float]] = None
        config_template: str | None = None
        local_context_data: Optional[Union[dict, None]] = None
        config_context: dict[str, str | None] = {}
        interface_count: int | None = None
        virtual_disk_count: int | None = None

    class SchemaIn(BaseModel):
        name: str = 'Virtual Machine Placeholder'
        role: int = Field(default_factory=lambda: Role(bootstrap_placeholder=True).id or 0)
        status: str = 'active'
        description: str | None = None
        serial: str | None = None
        tags: List[int] = Field(default_factory=lambda: [Tags(bootstrap_placeholder=True).id or 0])
        site: int | None = None
        cluster: int = Field(default_factory=lambda: Cluster(bootstrap_placeholder=True).id or 0)
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

    SchemaList = RootModel[List[Schema]]

    # NetBox API endpoint: /virtualization/virtual-machines/
    app: str = 'virtualization'
    name: str = 'virtual_machines'
    
    # Schema for objects
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    
    # Unique constraints for VirtualMachine objects
    unique_together = ['name']
    required_fields = ['name', 'status']

    # API
    prefix = '/virtual_machine'
    api_router = APIRouter(tags=['Virtualization / Virtual Machine'])
    