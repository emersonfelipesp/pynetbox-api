from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.dcim import Manufacturer
from pynetbox_api.dcim.manufacturer import (
    ManufacturerSchema,
    ManufacturerSchemaList,
    ManufacturerSchemaIn,
    Manufacturer
) 

manufacturer_router = APIRouter(tags=['DCIM / Manufacturer'])

from pynetbox_api.api import create_endpoints
create_endpoints(
    app=manufacturer_router,
    class_instance=Manufacturer
)
