from pynetbox_api.schemas.dcim import ManufacturerSchema
from pynetbox_api.session import NetBoxBase

class Manufacturer(NetBoxBase):
    app = 'dcim'
    name = 'manufacturers'
    schema = ManufacturerSchema
    unique_together = ['name', 'slug']