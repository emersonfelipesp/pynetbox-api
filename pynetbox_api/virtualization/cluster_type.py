from fastapi import APIRouter

from pynetbox_api.session import NetBoxBase

from pydantic import BaseModel, RootModel, AnyHttpUrl  
from typing import List, Optional, Union

from pynetbox_api.utils import GenericSchema, ValueLabelSchema
from pynetbox_api.dcim.interface import Interface, InterfaceBasicSchema
from pynetbox_api.extras import Tags, TagsSchema

__all__ = [
    'ClusterTypeBasicSchema',
    'ClusterTypeSchema',
    'ClusterTypeSchemaList',
    'ClusterTypeSchemaIn',
    'ClusterType'
]

class ClusterTypeBasicSchema(BaseModel):
    id: int | None = None
    url: AnyHttpUrl | None = None
    display: str  | None = None
    name: str | None = None
    slug: str | None = None
    description: str | None = None

class ClusterTypeSchema(GenericSchema, ClusterTypeBasicSchema):
    cluster_count: int | None = None

class ClusterTypeSchemaIn(BaseModel):
    name: str = 'Cluster Type Placeholder'
    slug: str = 'cluster-type-placeholder'
    description: str | None = None
    tags: List[int] = []

ClusterTypeSchemaList = RootModel[List[ClusterTypeSchema]]

class ClusterType(NetBoxBase):
    app: str = 'virtualization'
    name: str = 'cluster_types'
    schema = ClusterTypeSchema
    schema_in = ClusterTypeSchemaIn
    schema_list = ClusterTypeSchemaList
    unique_together = ['name', 'slug']
    required_fields = ['name', 'slug']
    
    # API
    prefix = '/cluster_type'
    api_router = APIRouter(tags=['Virtualization / Cluster Type'])