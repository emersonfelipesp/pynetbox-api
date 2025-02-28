from fastapi import APIRouter
from pynetbox_api.session import NetBoxBase

from pydantic import BaseModel, RootModel
from typing import List, Optional, Literal

from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.extras.tag import Tags

__all__ = [
    'DeviceType'
]

class DeviceType(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str | None = None
        manufacturer: Manufacturer.Schema
        model: str | None = None
        slug: str | None = None
        description: str | None = None


    class Schema(BasicSchema):
        display_url: str | None = None
        default_platform: str | None = None
        part_number: str | None = None
        u_height: int | None = None
        exclude_from_utilization: bool | None = None
        is_full_depth: bool | None = None
        subdevice_role: str | None = None
        airflow: str | None = None
        weight: int | None = None
        weight_unit: str | None = None
        front_image: str | None = None
        rear_image: str | None = None
        comments: str | None = None
        tags: List[Tags.Schema] | None = None
        custom_fields: dict[str, str | None] = {}
        created: str | None = None
        last_updated: str | None = None
        device_count: int | None = None
        console_port_template_count: int | None = None
        console_server_port_template_count: int | None = None
        power_port_template_count: int | None = None
        power_outlet_template_count: int | None = None
        interface_template_count: int | None = None
        front_port_template_count: int | None = None
        rear_port_template_count: int | None = None
        device_bay_template_count: int | None = None
        module_bay_template_count: int | None = None
        inventory_item_template_count: int | None = None


    class SchemaIn(BaseModel):
        manufacturer: int = Manufacturer(bootstrap_placeholder=True).get('id', 0)
        model: str = 'Device Type Placeholder'
        slug: str = 'device-type-placeholder'
        default_platform: str | None = None
        description: str = 'Placeholder object for ease data ingestion'
        tags: List[int] = [Tags(bootstrap_placeholder=True).get('id', 0)]
        u_height: float = 1
        part_number: str | None = None
        subdevice_role: str = Optional[Literal['parent', 'child', None]]
        airflow: str | None = None
        weight: str | None = None
        weight_unit: Optional[Literal['kg', 'g', 'lb', 'oz', None]]
        front_image: str | None = None
        rear_image: str | None = None
        comments: str | None = None

    SchemaList = RootModel[List[Schema]]

    app = 'dcim'
    name = 'device_types'
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    unique_together = ['manufacturer', 'model', 'slug']

    # API
    prefix = '/device_type'
    api_router = APIRouter(tags=['DCIM / Device Type'])