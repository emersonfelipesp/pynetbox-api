from fastapi import APIRouter
from pydantic import BaseModel, RootModel, AnyHttpUrl
from typing import List
from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase

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
    # NetBox API endpoint: /api/virtualization/cluster-groups/
    app: str = 'virtualization'
    name: str = 'cluster_groups'
    
    # Schema definitions
    schema = ClusterGroupSchema
    schema_in = ClusterGroupSchemaIn
    schema_list = ClusterGroupSchemaList
    
    # Unique constraints
    unique_together = ['name', 'slug']
    required_fields = ['name', 'slug']
    
    # API
    prefix = '/cluster_group'
    api_router = APIRouter(tags=['Virtualization / Cluster Group'])