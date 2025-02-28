from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List
from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase

__all__ = [
    'ClusterType'
]



class ClusterType(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str  | None = None
        name: str | None = None
        slug: str | None = None
        description: str | None = None

    class Schema(GenericSchema, BasicSchema):
        cluster_count: int | None = None

    class SchemaIn(BaseModel):
        name: str = 'Cluster Type Placeholder'
        slug: str = 'cluster-type-placeholder'
        description: str | None = None
        tags: List[int] = []

    SchemaList = RootModel[List[Schema]]
    
    app: str = 'virtualization'
    name: str = 'cluster_types'
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    unique_together = ['name', 'slug']
    required_fields = ['name', 'slug']
    
    # API
    prefix = '/cluster_type'
    api_router = APIRouter(tags=['Virtualization / Cluster Type'])