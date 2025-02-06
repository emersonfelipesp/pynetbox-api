from pynetbox_api.schemas.dcim import (
    ManufacturerSchema,
    ManufacturerSchemaIn,
    ManufacturerSchemaList,
    DeviceRoleSchema,
    DeviceRoleSchemaIn,
    DeviceRoleSchemaList
)
from pynetbox_api.session import NetBoxBase

class Manufacturer(NetBoxBase):
    app = 'dcim'
    name = 'manufacturers'
    schema = ManufacturerSchema
    schema_in = ManufacturerSchemaIn
    schema_list = ManufacturerSchemaList
    unique_together = ['name', 'slug']
    
class DeviceRole(NetBoxBase):
    app = 'dcim'
    name = 'device_roles'
    schema = DeviceRoleSchema
    schema_in = DeviceRoleSchemaIn
    schema_list = DeviceRoleSchemaList
    unique_together = ['name', 'slug']