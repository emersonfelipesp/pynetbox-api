from fastapi import APIRouter

from pynetbox_api.session import NetBoxBase

from pydantic import BaseModel, RootModel, AnyHttpUrl  
from typing import List, Optional, Union

from pynetbox_api.utils import GenericSchema, ValueLabelSchema
from pynetbox_api.dcim.interface import Interface, InterfaceBasicSchema
from pynetbox_api.extras import Tags, TagsSchema

__all__ = [
    'ClusterGroupBasicSchema',
    'ClusterGroupSchema',
    'ClusterGroupSchemaList',
    'ClusterGroupSchemaIn',
    'ClusterGroup'
]

class ClusterGroupBasicSchema(BaseModel):
    id: int | None = None
    url: AnyHttpUrl | None = None
    display: str  | None = None
    name: str | None = None
    slug: str | None = None
    description: str | None = None

class ClusterGroupSchema(GenericSchema, ClusterGroupBasicSchema):
    cluster_count: int | None = None

class ClusterGroupSchemaIn(BaseModel):
    name: str = 'Cluster Group Placeholder'
    slug: str = 'cluster-group-placeholder'
    description: str | None = None
    tags: List[int] = []
    
ClusterGroupSchemaList = RootModel[List[ClusterGroupSchema]]

class ClusterGroup(NetBoxBase):
    app: str = 'virtualization'
    name: str = 'cluster_groups'
    schema = ClusterGroupSchema
    schema_in = ClusterGroupSchemaIn
    schema_list = ClusterGroupSchemaList
    unique_together = ['name', 'slug']
    required_fields = ['name', 'slug']
    
    # API
    prefix = '/cluster_group'
    api_router = APIRouter(tags=['Virtualization / Cluster Group'])