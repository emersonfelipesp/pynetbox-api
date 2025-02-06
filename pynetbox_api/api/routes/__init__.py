from fastapi import APIRouter
from pynetbox_api.api.routes.dcim import dcim_router
from pynetbox_api.api.routes.extras import extras_router

netbox_router = APIRouter()
netbox_router.include_router(dcim_router, prefix='/dcim')
netbox_router.include_router(extras_router, prefix='/extras')
