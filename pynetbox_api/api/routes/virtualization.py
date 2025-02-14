from fastapi import APIRouter
from pynetbox_api.api import create_endpoints
from pynetbox_api.virtualization.cluster import (
    ClusterType, ClusterGroup, Cluster,
)

from pynetbox_api.virtualization.virtual_disk import VirtualDisk
from pynetbox_api.virtualization.interface import VMInterface, VirtualMachine

virtualization_router = APIRouter()
for router in [ClusterType, ClusterGroup, Cluster, VirtualMachine, VirtualDisk, VMInterface]:
    # Create the endpoints for each router, using only the class_instance.
    create_endpoints(router)
    virtualization_router.include_router(router.api_router, prefix=router.prefix)
