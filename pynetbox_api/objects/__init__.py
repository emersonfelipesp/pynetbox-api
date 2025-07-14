from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.dcim.device_type import DeviceType
from pynetbox_api.dcim.device import Device
from pynetbox_api.dcim.device_role import DeviceRole
from pynetbox_api.dcim.site import Site

class DcimObjects:
    def __init__(self, api):
        self.api = api
        self.manufacturers = Manufacturer(nb=api.session)
        self.device_types = DeviceType(nb=api.session)
        self.device_roles = DeviceRole(nb=api.session)
        self.devices = Device(nb=api.session)
        self.sites = Site(nb=api.session)
        