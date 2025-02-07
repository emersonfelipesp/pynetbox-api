from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.dcim import Manufacturer
from pynetbox_api.schemas.dcim.manufacturer import (
    ManufacturerSchema,
    ManufacturerSchemaList,
    ManufacturerSchemaIn
) 

manufacturer_router = APIRouter(tags=['DCIM / Manufacturer'])

@manufacturer_router.get('/', response_model=ManufacturerSchemaList)
async def get_manufacturers() -> ManufacturerSchemaList:
    return Manufacturer().all()

@manufacturer_router.get("/{manufacturer_id}")
async def get_manufacturer(manufacturer_id: int) -> ManufacturerSchema:
    return Manufacturer().get(id=manufacturer_id)

@manufacturer_router.post("/", response_model=ManufacturerSchema)
async def create_manufacturer(manufacturer: ManufacturerSchemaIn) -> ManufacturerSchema:
    return Manufacturer(**manufacturer.model_dump(exclude_unset=True))

@manufacturer_router.post('/placeholder', response_model=ManufacturerSchema)
async def create_manufacturer_placeholder(use_placeholder: Annotated[bool | None, Query()] = True) -> ManufacturerSchema:
    return Manufacturer(use_placeholder=use_placeholder).object

@manufacturer_router.put("/{manufacturer_id}")
async def update_manufacturer(manufacturer_id: int, manufacturer: ManufacturerSchema) -> JSONResponse:
    return Manufacturer().update(id=manufacturer_id, json=manufacturer.model_dump(exclude_unset=True))

@manufacturer_router.delete("/{manufacturer_id}")
async def delete_manufacturer(manufacturer_id: int) -> JSONResponse:
    return Manufacturer().delete(id=manufacturer_id)
