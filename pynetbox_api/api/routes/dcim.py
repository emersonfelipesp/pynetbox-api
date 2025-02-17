from fastapi import APIRouter
from pynetbox_api.api import create_endpoints
from pynetbox_api.dcim.device import Device, DeviceType, Site, DeviceRole
from pynetbox_api.dcim.platform import Platform
from pynetbox_api.dcim.manufacturer import Manufacturer

dcim_router = APIRouter()
for router in [Site, Manufacturer, DeviceRole, DeviceType, Device, Platform]:
    # Create the endpoints for each router, using only the class_instance.
    create_endpoints(router)
    dcim_router.include_router(router.api_router, prefix=router.prefix)