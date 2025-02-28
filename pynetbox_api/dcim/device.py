from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.session import NetBoxBase
from pynetbox_api.dcim.site import Site
from pynetbox_api.dcim.device_role import DeviceRole
from pynetbox_api.dcim.device_type import DeviceType
from pynetbox_api.extras.tag import Tags
from pynetbox_api.virtualization.cluster import Cluster

class Device(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str | None = None
        name: str | None = None
        description: str | None = None
        
    class Schema(BasicSchema):
        display_url: str
        name: str
        device_type: DeviceType.BasicSchema
        role: DeviceRole.BasicSchema
        tenant: bool | None = None
        platform: str | None = None
        serial: str | None = None
        asset_tag: str | None = None
        site: Site.Schema
        location: str | None = None
        rack: str | None = None
        position: int | None = None
        face: str | None = None
        latitude: float | None = None
        longitude: float | None = None
        status: NetBoxBase.StatusSchema
        airflow: str | None = None
        primary_ip: str | None = None
        primary_ip4: str | None = None
        primary_ip6: str | None = None
        oob_ip: str | None = None
        cluster: Cluster.BasicSchema | None = None
        virtual_chassis: str | None = None
        vc_position: int | None = None
        vc_priority: int | None = None
        comments: str | None = None
        config_template: str | None = None
        config_context: dict[str, str | None] = {}
        local_context_data: str | None = None
        tags: List[Tags.Schema] = []
        custom_fields: dict[str, str | None] = {}
        created: str | None = None
        last_updated: str | None = None
        console_port_count: int | None = None
        console_server_port_count: int | None = None
        power_port_count: int | None = None
        power_outlet_count: int | None = None
        interface_count: int | None = None
        front_power_port_count: int | None = None
        rear_power_port_count: int | None = None
        device_bay_count: int | None = None
        module_bay_count: int | None = None
        inventory_items: int | None = None

    class SchemaIn(BaseModel):
        name: str = 'Device Placeholder'
        role: int = DeviceRole(bootstrap_placeholder=True).get('id', 0)
        description: str = 'Placeholder object for ease data ingestion'
        tags: List[int] = [Tags(bootstrap_placeholder=True).get('id', 0)]
        device_type: int = DeviceType(bootstrap_placeholder=True).get('id', 0)
        airflow: str | None = None
        serial: str | None = None
        asset_tag: str | None = None
        site: int = Site(bootstrap_placeholder=True).get('id', 0)
        location: str | None = None
        position: int | None = None
        rack: str | None = None
        face: str | None = None
        latitude: float | None = None
        longitude: float | None = None
        status: str = 'active'
        platform: str
        config_template: str | None = None
        cluster: int | None = None
        tenant_group: str | None = None
        tenant: str | None = None
        virtual_chassis: str | None = None
        position: int | None = None
        priority: int | None = None
        custom_fields: dict[str, str | None] = {}

    SchemaList = RootModel[List[Schema]]
    app = 'dcim'
    name = 'devices'
    schema = Schema
    schema_basic = BasicSchema
    schema_in = SchemaIn
    schema_list = SchemaList
    unique_together = ['name']
    
    # API
    prefix = '/device'
    api_router = APIRouter(tags=['DCIM / Device'])