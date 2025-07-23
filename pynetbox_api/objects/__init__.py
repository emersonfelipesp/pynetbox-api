# DCIM Objects
from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.dcim.device_type import DeviceType
from pynetbox_api.dcim.device import Device
from pynetbox_api.dcim.device_role import DeviceRole
from pynetbox_api.dcim.site import Site

# Virtualization Objects
from pynetbox_api.virtualization.virtual_machine import VirtualMachine
from pynetbox_api.virtualization.cluster import Cluster
from pynetbox_api.virtualization.cluster_type import ClusterType
from pynetbox_api.virtualization.cluster_group import ClusterGroup

# Objects
class DcimObjects:
    def __init__(self, api):
        self.api = api
        self.manufacturers = Manufacturer(nb=api.session)
        self.device_types = DeviceType(nb=api.session)
        self.device_roles = DeviceRole(nb=api.session)
        self.devices = Device(nb=api.session)
        self.sites = Site(nb=api.session)
    
class VirtualizationObjects:
    def __init__(self, api):
        self.api = api
        self.virtual_machines = VirtualMachine(nb=api.session)
        self.clusters = Cluster(nb=api.session)
        self.cluster_types = ClusterType(nb=api.session)
        self.cluster_groups = ClusterGroup(nb=api.session)
        self.cluster_types = ClusterType(nb=api.session)