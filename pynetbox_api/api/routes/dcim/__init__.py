from fastapi import APIRouter
from pynetbox_api.api.routes.dcim.manufacturer import manufacturer_router

dcim_router = APIRouter(tags=['DCIM'])
dcim_router.include_router(manufacturer_router, prefix="/manufacturer")