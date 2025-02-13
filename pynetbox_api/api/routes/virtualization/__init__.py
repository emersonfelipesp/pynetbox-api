from fastapi import APIRouter

from pynetbox_api.api.routes.virtualization.cluster_type import cluster_type_router

virtualization_router = APIRouter()
virtualization_router.include_router(cluster_type_router, prefix="/cluster_type")