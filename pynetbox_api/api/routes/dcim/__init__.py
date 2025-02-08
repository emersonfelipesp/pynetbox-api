from fastapi import APIRouter
from pynetbox_api.api.routes.dcim.manufacturer import manufacturer_router
from pynetbox_api.api.routes.dcim.device_role import device_role_router
from pynetbox_api.api.routes.dcim.device_type import device_type_router

dcim_router = APIRouter()
dcim_router.include_router(manufacturer_router, prefix="/manufacturer")
dcim_router.include_router(device_role_router, prefix="/device_role")
dcim_router.include_router(device_type_router, prefix="/device_type")