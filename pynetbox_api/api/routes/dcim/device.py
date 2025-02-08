from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.dcim.device import (
    DeviceSchema,
    DeviceSchemaList,
    DeviceSchemaIn,
    Device
)

device_router = APIRouter(tags=['DCIM / Device'])

@device_router.get('/', response_model=DeviceSchemaList)
async def get_device_types() -> DeviceSchemaList:
    return Device().all()

@device_router.get('/{device_id}')
async def get_device_type(device_id: int) -> DeviceSchema:
    return Device().get(id=device_id)

@device_router.post('/', response_model=DeviceSchema)
async def create_device_type(device_type: DeviceSchemaIn) -> DeviceSchema:
    return Device(**device_type.model_dump(exclude_unset=True))

@device_router.post('/placeholder', response_model=DeviceSchema)
async def create_device_type_placeholder(use_placeholder: Annotated[bool | None, Query()] = True) -> DeviceSchema:
    return Device(use_placeholder=use_placeholder).object

@device_router.put('/{device_id}')
async def update_device_type(device_id: int, device_type: DeviceSchema) -> JSONResponse:
    return Device().update(id=device_id, json=device_type.model_dump(exclude_unset=True))

@device_router.delete('/{device_id}')
async def delete_device_type(device_id: int) -> JSONResponse:
    return Device().delete(id=device_id)