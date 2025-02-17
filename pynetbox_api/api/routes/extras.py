from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.extras.tag import Tags
from pynetbox_api.extras.custom_field import CustomField, CustomFieldChoice

from pynetbox_api.api import create_endpoints
extras_router = APIRouter()

for router in [Tags, CustomField, CustomFieldChoice]:
    create_endpoints(router)
    extras_router.include_router(router.api_router, prefix=router.prefix)