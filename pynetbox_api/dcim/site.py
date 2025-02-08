from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.session import NetBoxBase
from pynetbox_api.extras import Tags, TagsSchema
from pynetbox_api.utils import StatusSchema
__all__ = [
    "SiteSchema",
    "SiteSchemaList",
    "SiteSchemaIn",
    "Site"
]

class SiteSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display: str | None = None
    display_url: str | None = None
    name: str | None = None
    slug: str | None = None
    status: StatusSchema | None = None
    region: str | None = None
    group: str | None = None
    tenant: str | None = None
    facility: str | None = None
    time_zone: str | None = None
    description: str | None = None
    physical_address: str | None = None
    shipping_address: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    comments: str | None = None
    asns: list | None = None
    tags: List[TagsSchema] | None = None
    custom_fields: dict[str, str | None] = {}
    created: str | None = None
    last_updated: str | None = None
    circuit_count: int | None = None
    device_count: int | None = None
    rack_count: int | None = None
    virtualmachine_count: int | None = None
    vlan_count: int | None = None

class SiteSchemaIn(BaseModel):
    name: str = 'Site Placeholder'
    slug: str = 'site-placeholder'
    status: str = 'active'
    region: str | None = None
    group: str | None = None
    facility: str | None = None
    asns: list | None = None
    time_zone: str | None = None
    description: str = 'Placeholder object for ease data ingestion'
    tags: List[int] = [Tags(use_placeholder=True).object['id']]
    tenant_group: str | None = None
    tenant: str | None = None
    physical_address: str | None = None
    shipping_address: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    comments: str | None = None

SiteSchemaList = RootModel[List[SiteSchema]]

class Site(NetBoxBase):
    app = 'dcim'
    name = 'sites'
    schema = SiteSchema
    schema_in = SiteSchemaIn
    schema_list = SiteSchemaList
    unique_together = ['name', 'slug']