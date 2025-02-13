from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.extras import Tags
from pynetbox_api.api import create_endpoints
extras_router = APIRouter()

for router in [Tags]:
    create_endpoints(router)
    extras_router.include_router(router.api_router, prefix=router.prefix)