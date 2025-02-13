from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.dcim.device_role import (
    DeviceRoleSchema,
    DeviceRoleSchemaList,
    DeviceRoleSchemaIn,
    DeviceRole
)

device_role_router = APIRouter(tags=['DCIM / Device Role'])

@device_role_router.get('/', response_model=DeviceRoleSchemaList)
async def get_device_roles() -> DeviceRoleSchemaList:
    return DeviceRole().all()

@device_role_router.post('/placeholder', response_model=DeviceRoleSchema)
async def create_device_role_placeholder() -> DeviceRoleSchema:
    return DeviceRole(bootstrap_placeholder=True).result

@device_role_router.get('/{device_role_id}')
async def get_device_role(device_role_id: int) -> DeviceRoleSchema:
    return DeviceRole().get(id=device_role_id)

@device_role_router.post('/', response_model=DeviceRoleSchema)
async def create_device_role(device_role: DeviceRoleSchemaIn) -> DeviceRoleSchema:
    return DeviceRole(**device_role.model_dump(exclude_unset=True))

@device_role_router.put('/{device_role_id}')
async def update_device_role(device_role_id: int, device_role: DeviceRoleSchema) -> JSONResponse:
    return DeviceRole().update(id=device_role_id, json=device_role.model_dump(exclude_unset=True))

@device_role_router.delete('/{device_role_id}')
async def delete_device_role(device_role_id: int) -> JSONResponse:
    return DeviceRole().delete(id=device_role_id)