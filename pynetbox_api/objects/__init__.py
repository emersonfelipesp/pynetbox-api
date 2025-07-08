from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.dcim.device_type import DeviceType
from pynetbox_api.dcim.device import Device
from pynetbox_api.dcim.device_role import DeviceRole
from pynetbox_api.dcim.site import Site

class DcimObjects:
    def __init__(self, api):
        self.api = api
        self.manufacturer = Manufacturer(nb=api.session)
        self.device_type = DeviceType(nb=api.session)
        self.device_role = DeviceRole(nb=api.session)
        self.device = Device(nb=api.session)
        self.site = Site(nb=api.session)
        