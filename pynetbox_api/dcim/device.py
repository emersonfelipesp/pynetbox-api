from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.session import NetBoxBase
from pynetbox_api.dcim.site import Site, SiteSchema
from pynetbox_api.dcim.device_role import DeviceRole, DeviceRoleBasicSchema
from pynetbox_api.dcim.device_type import DeviceType, DeviceTypeBasicSchema
from pynetbox_api.extras import Tags, TagsSchema
from pynetbox_api.utils import StatusSchema

class DeviceBasicSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display: str | None = None
    name: str | None = None
    description: str | None = None
    
class DeviceSchema(DeviceBasicSchema):
    display_url: str
    name: str
    device_type: DeviceTypeBasicSchema
    role: DeviceRoleBasicSchema
    tenant: bool | None = None
    platform: str | None = None
    serial: str | None = None
    asset_tag: str | None = None
    site: SiteSchema
    location: str | None = None
    rack: str | None = None
    position: int | None = None
    face: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    status: StatusSchema
    airflow: str | None = None
    primary_ip: str | None = None
    primary_ip4: str | None = None
    primary_ip6: str | None = None
    oob_ip: str | None = None
    cluster: str | None = None
    virtual_chassis: str | None = None
    vc_position: int | None = None
    vc_priority: int | None = None
    comments: str | None = None
    config_template: str | None = None
    config_context: dict[str, str | None] = {}
    local_context_data: str | None = None
    tags: List[TagsSchema] = []
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

class DeviceSchemaIn(BaseModel):
    name: str = 'Device Placeholder'
    role: int = DeviceRole(bootstrap_placeholder=True).result.get('id')
    description: str = 'Placeholder object for ease data ingestion'
    tags: List[int] = [Tags(bootstrap_placeholder=True).result.get('id')]
    device_type: int = DeviceType(bootstrap_placeholder=True).result.get('id')
    airflow: str | None = None
    serial: str | None = None
    asset_tag: str | None = None
    site: int = Site(bootstrap_placeholder=True).result.get('id')
    location: str | None = None
    position: int | None = None
    rack: str | None = None
    face: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    status: str = 'active'
    platform: str
    config_template: str | None = None
    cluster: str | None = None
    tenant_group: str | None = None
    tenant: str | None = None
    virtual_chassis: str | None = None
    position: int | None = None
    priority: int | None = None
    custom_fields: dict[str, str | None] = {}

DeviceSchemaList = RootModel[List[DeviceSchema]]

class Device(NetBoxBase):
    app = 'dcim'
    name = 'devices'
    schema = DeviceSchema
    schema_in = DeviceSchemaIn
    schema_list = DeviceSchemaList
    unique_together = ['name']