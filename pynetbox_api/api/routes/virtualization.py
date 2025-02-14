from fastapi import APIRouter
from pynetbox_api.api import create_endpoints
from pynetbox_api.virtualization import (
    ClusterType, ClusterGroup, Cluster,
    VirtualMachine, VirtualDisk
)

virtualization_router = APIRouter()
for router in [ClusterType, ClusterGroup, Cluster, VirtualMachine, VirtualDisk]:
    # Create the endpoints for each router, using only the class_instance.
    create_endpoints(router)
    virtualization_router.include_router(router.api_router, prefix=router.prefix)
