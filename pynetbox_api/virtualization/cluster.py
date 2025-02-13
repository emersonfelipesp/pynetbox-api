from fastapi import APIRouter
from pydantic import BaseModel, RootModel, AnyHttpUrl
from typing import List
from pynetbox_api.utils import GenericSchema, StatusSchema
from pynetbox_api.virtualization.cluster_type import ClusterType, ClusterTypeBasicSchema
from pynetbox_api.virtualization.cluster_group import ClusterGroupBasicSchema
from pynetbox_api.session import NetBoxBase

__all__ = [
    'ClusterBasicSchema',
    'ClusterSchema',
    'ClusterSchemaList',
    'ClusterSchemaIn',
    'Cluster'
]

class ClusterBasicSchema(BaseModel):
    id: int | None = None
    url: AnyHttpUrl | None = None
    display: str  | None = None
    name: str | None = None
    description: str | None = None

class ClusterSchema(GenericSchema, ClusterBasicSchema):
    type: ClusterTypeBasicSchema
    group: ClusterGroupBasicSchema | None = None
    status: StatusSchema
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

class ClusterSchemaIn(BaseModel):
    name: str = 'Cluster Placeholder'
    type: int = ClusterType(bootstrap_placeholder=True).id
    group: int | None = None
    status: str = 'active'
    description: str | None = None
    tags: List[int] = []
    scope_type: str | None = None
    scope_id: int | None = None
    tenant_group: str | None = None
    tenant: str | None = None
    comments: str | None = None

ClusterSchemaList = RootModel[List[ClusterSchema]]

class Cluster(NetBoxBase):
    # NetBox API endpoint: /api/virtualization/clusters/
    app: str = 'virtualization'
    name: str = 'clusters'
    
    # Schema definitions
    schema = ClusterSchema
    schema_in = ClusterSchemaIn
    schema_list = ClusterSchemaList
    
    # Unique constraints
    unique_together = ['name']
    required_fields = ['name', 'type', 'status']
    
    # API
    prefix = '/cluster'
    api_router = APIRouter(tags=['Virtualization / Cluster'])
