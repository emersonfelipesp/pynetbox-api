from pynetbox_api.dcim.manufacturer import Manufacturer

class DcimObjects:
    def __init__(self, api):
        self.api = api
        self.manufacturer = Manufacturer(nb=api.session)