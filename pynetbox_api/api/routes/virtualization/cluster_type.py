from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.virtualization.cluster_type import (
    ClusterTypeSchema,
    ClusterTypeSchemaList,
    ClusterTypeSchemaIn,
    ClusterType
)

device_type_router = APIRouter(tags=['DCIM / Device Type'])

@device_type_router.get('/', response_model=ClusterTypeSchemaList)
async def get_device_types() -> ClusterTypeSchemaList:
    return ClusterType().all()

@device_type_router.get('/{device_type_id}')
async def get_device_type(device_type_id: int) -> ClusterTypeSchema:
    return ClusterType().get(id=device_type_id)

@device_type_router.post('/', response_model=ClusterTypeSchema)
async def create_device_type(device_type: ClusterTypeSchemaIn) -> ClusterTypeSchema:
    return ClusterType(**device_type.model_dump(exclude_unset=True))

@device_type_router.post('/placeholder', response_model=ClusterTypeSchema)
async def create_device_type_placeholder(use_placeholder: Annotated[bool | None, Query()] = True) -> ClusterTypeSchema:
    return ClusterType(use_placeholder=use_placeholder).object

@device_type_router.put('/{device_type_id}')
async def update_device_type(device_type_id: int, device_type: ClusterTypeSchema) -> JSONResponse:
    return ClusterType().update(id=device_type_id, json=device_type.model_dump(exclude_unset=True))

@device_type_router.delete('/{device_type_id}')
async def delete_device_type(device_type_id: int) -> JSONResponse:
    return ClusterType().delete(id=device_type_id)