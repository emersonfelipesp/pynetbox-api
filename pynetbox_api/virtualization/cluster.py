from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List
from pynetbox_api.utils import GenericSchema
from pynetbox_api.virtualization.cluster_type import ClusterType
from pynetbox_api.virtualization.cluster_group import ClusterGroup
from pynetbox_api.session import NetBoxBase

__all__ = [
    'ClusterBasicSchema',
    'ClusterSchema',
    'ClusterSchemaList',
    'ClusterSchemaIn',
    'Cluster'
]

class Cluster(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str  | None = None
        name: str | None = None
        description: str | None = None

    class Schema(GenericSchema, BasicSchema):
        type: ClusterType.BasicSchema
        group: ClusterGroup.BasicSchema | None = None
        status: NetBoxBase.StatusSchema
        tenant_group: str | None = None
        tenant: str | None = None # TODO: TenantBasicSchema
        scope_type: str | None = None
        scope_id: int | None = None
        scope: str | None = None
        description: str | None = None
        comments: str | None = None
        device_count: int | None = None
        virtualmachine_count: int | None = None
        allocated_vcpus: int | None = None
        allocated_memory: int | None = None
        allocated_disk: int | None = None

    class SchemaIn(BaseModel):
        name: str = 'Cluster Placeholder'
        type: int = ClusterType(bootstrap_placeholder=True).get('id', 0)
        group: int | None = None
        status: str = 'active'
        description: str | None = None
        tags: List[int] = []
        scope_type: str | None = None
        scope_id: int | None = None
        tenant_group: str | None = None
        tenant: str | None = None
        comments: str | None = None

    SchemaList = RootModel[List[Schema]]
    
    # NetBox API endpoint: /api/virtualization/clusters/
    app: str = 'virtualization'
    name: str = 'clusters'
    
    # Schema definitions
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    
    # Unique constraints
    unique_together = ['name']
    required_fields = ['name', 'type', 'status']
    
    # API
    prefix = '/cluster'
    api_router = APIRouter(tags=['Virtualization / Cluster'])
