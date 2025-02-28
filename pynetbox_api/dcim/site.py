from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.session import NetBoxBase
from pynetbox_api.extras.tag import Tags

__all__ = [
    "Site"
]

class Site(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str | None = None
        name: str | None = None
        slug: str | None = None

    class Schema(BasicSchema):
        display_url: str | None = None
        status: NetBoxBase.StatusSchema | None = None
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
        tags: List[Tags.Schema] | None = None
        custom_fields: dict[str, str | None] = {}
        created: str | None = None
        last_updated: str | None = None
        circuit_count: int | None = None
        device_count: int | None = None
        rack_count: int | None = None
        virtualmachine_count: int | None = None
        vlan_count: int | None = None

    class SchemaIn(BaseModel):
        name: str = 'Site Placeholder'
        slug: str = 'site-placeholder'
        status: str = 'active'
        region: str | None = None
        group: str | None = None
        facility: str | None = None
        asns: list | None = None
        time_zone: str | None = None
        description: str = 'Placeholder object for ease data ingestion'
        tags: List[int] = [Tags(bootstrap_placeholder=True).get('id', 0)]
        tenant_group: str | None = None
        tenant: str | None = None
        physical_address: str | None = None
        shipping_address: str | None = None
        latitude: str | None = None
        longitude: str | None = None
        comments: str | None = None

    SchemaList = RootModel[List[Schema]]

    app = 'dcim'
    name = 'sites'
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    unique_together = ['name', 'slug']
    
    # API
    prefix = '/site'
    api_router = APIRouter(tags=['DCIM / '])