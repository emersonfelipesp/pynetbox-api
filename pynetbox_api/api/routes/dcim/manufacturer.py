from fastapi import APIRouter
from pynetbox_api.dcim import Manufacturer

manufacturer_router = APIRouter()

@manufacturer_router.get("/{manufacturer_id}")
async def get_manufacturers(manufacturer_id: int):
    return Manufacturer().get(id=manufacturer_id)