from fastapi import APIRouter
from pydantic import BaseModel, RootModel, AnyHttpUrl
from typing import List
from pynetbox_api.utils import GenericSchema
from pynetbox_api.session import NetBoxBase

__all__ = [
    'VirtualDiskBasicSchema',
    'VirtualDiskSchema',
    'VirtualDiskSchemaList',
    'VirtualDiskSchemaIn',
    'VirtualDisk'
]