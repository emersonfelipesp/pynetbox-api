from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.api import create_endpoints, HTTPMethod

from pynetbox_api.dcim.device_type import DeviceType

device_type_router = APIRouter(tags=['DCIM / Device Type'])

create_endpoints(
    app=device_type_router,  
    class_instance=DeviceType,
)