from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from pynetbox_api.dcim.site import (
    SiteSchema,
    SiteSchemaList,
    SiteSchemaIn,
    Site
) 

site_router = APIRouter(tags=['DCIM / Site'])

@site_router.get('/', response_model=SiteSchemaList)
async def get_sites() -> SiteSchemaList:
    return Site().all()

@site_router.get("/{site_id}")
async def get_site(site_id: int) -> SiteSchema:
    return Site().get(id=site_id)

@site_router.post("/", response_model=SiteSchema)
async def create_site(site: SiteSchemaIn) -> SiteSchema:
    return Site(**site.model_dump(exclude_unset=True))

@site_router.post('/placeholder', response_model=SiteSchema)
async def create_site_placeholder(use_placeholder: Annotated[bool | None, Query()] = True) -> SiteSchema:
    return Site(use_placeholder=use_placeholder).object

@site_router.put("/{site_id}")
async def update_site(site_id: int, site: SiteSchema) -> JSONResponse:
    return Site().update(id=site_id, json=site.model_dump(exclude_unset=True))

@site_router.delete("/{site_id}")
async def delete_site(site_id: int) -> JSONResponse:
    return Site().delete(id=site_id)
