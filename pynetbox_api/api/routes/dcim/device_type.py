from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.dcim.device_type import (
    DeviceTypeSchema,
    DeviceTypeSchemaList,
    DeviceTypeSchemaIn,
    DeviceType
)

device_type_router = APIRouter(tags=['DCIM / Device Role'])

@device_type_router.get('/', response_model=DeviceTypeSchemaList)
async def get_device_types() -> DeviceTypeSchemaList:
    return DeviceType().all()

@device_type_router.get('/{device_type_id}')
async def get_device_type(device_type_id: int) -> DeviceTypeSchema:
    return DeviceType().get(id=device_type_id)

@device_type_router.post('/', response_model=DeviceTypeSchema)
async def create_device_type(device_type: DeviceTypeSchemaIn) -> DeviceTypeSchema:
    return DeviceType(**device_type.model_dump(exclude_unset=True))

@device_type_router.post('/placeholder', response_model=DeviceTypeSchema)
async def create_device_type_placeholder(use_placeholder: Annotated[bool | None, Query()] = True) -> DeviceTypeSchema:
    return DeviceType(use_placeholder=use_placeholder).object

@device_type_router.put('/{device_type_id}')
async def update_device_type(device_type_id: int, device_type: DeviceTypeSchema) -> JSONResponse:
    return DeviceType().update(id=device_type_id, json=device_type.model_dump(exclude_unset=True))

@device_type_router.delete('/{device_type_id}')
async def delete_device_type(device_type_id: int) -> JSONResponse:
    return DeviceType().delete(id=device_type_id)