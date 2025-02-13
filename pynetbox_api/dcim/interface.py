from pydantic import BaseModel, RootModel, HttpUrl, AnyHttpUrl
from typing import List, Optional, Union

from pynetbox_api.dcim.device import Device, DeviceBasicSchema
from pynetbox_api.session import NetBoxBase
from pynetbox_api.extras import TagsSchema, Tags
from pynetbox_api.utils import GenericSchema, ValueLabelSchema

__all__ = [
    "InterfaceBasicSchema",
    "InterfaceSchema",
    "InterfaceSchemaList",
    "InterfaceSchemaIn",
    "Interface"
]

class InterfaceBasicSchema(BaseModel):
    id: int | None = None
    url: AnyHttpUrl | None = None
    display: str | None = None
    name: str | None = None
    description: str | None = None
    device: DeviceBasicSchema
    cable: Optional[Union[str, None]] = None
    _occupied: bool | None = None
    
class InterfaceSchema(InterfaceBasicSchema, GenericSchema):
    display_url: str | None = None
    vdcs: List[str] | None = None
    module: str | None = None
    label: str | None = None
    type: ValueLabelSchema
    enabled: bool | None = None
    bridge: str | None = None
    lag: str | None = None
    mtu: int | None = None
    mac_address: str | None = None
    primary_mac_address: str | None = None
    mac_addresses: List[str] | None = None
    speed: int | None = None
    duplex: str | None = None
    wwn: str | None = None
    mgmt_only: bool | None = None
    mode: str | None = None
    rf_role: str | None = None
    rf_channel: str | None = None
    poe_mode: str | None = None
    poe_type: str | None = None
    rf_channel_frequency: str | None = None
    rf_channel_width: str | None = None
    tx_power: str | None = None
    untagged_vlan: str | None = None
    tagged_vlans: List[str] | None = None
    qinq_svlan: str | None = None
    vlan_translation_policy: Optional[Union[str, None]] = None
    mark_connected: bool | None = None
    cable_end: Optional[Union[str, None]] = None
    wireless_link: Optional[Union[str, None]] = None
    link_peers: List = []
    link_peers_type: Optional[Union[str, None]] = None
    wireless_lans: List = []
    vrf: Optional[Union[str, None]] = None
    l2vpn_termination: Optional[Union[str, None]] = None
    connected_endpoints: Optional[Union[str, None]] = None
    connected_endpoints_type: Optional[Union[str, None]] = None
    connected_endpoints_reachable: Optional[Union[str, None]] = None
    count_ipaddresses: int | None = None
    count_fhrp_groups: int | None = None

class InterfaceSchemaIn(BaseModel):
    device: int = Device(bootstrap_placeholder=True).id
    name: str = 'Interface Placeholder'
    type: str = 'other'
    enabled: bool = True
    description: str = 'Interface Placeholder'
    tags: List[int] = [Tags(bootstrap_placeholder=True).id]

InterfaceSchemaList = RootModel[List[InterfaceSchema]]

class Interface(NetBoxBase):
    app = 'dcim'
    name = 'interfaces'
    schema = InterfaceSchema
    schema_in = InterfaceSchemaIn
    schema_list = InterfaceSchemaList
    unique_together = ['device', 'name']
    required_fields = ['device', 'name', 'type']