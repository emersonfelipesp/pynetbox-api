from fastapi import APIRouter
from pydantic import BaseModel, RootModel
from typing import List, Optional, Union, Any
from pynetbox_api.utils import GenericSchema
from pynetbox_api.virtualization.cluster import Cluster
from pynetbox_api.dcim.site import Site
from pynetbox_api.dcim.device_role import DeviceRole as Role
from pynetbox_api.session import NetBoxBase
from pynetbox_api.ipam.ip_address import IPAddress
from pynetbox_api.dcim.device import Device
    
__all__ = [
    'CustomField',
    'CustomFieldChoice'
]

class CustomFieldChoice(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str  | None = None
        name: str | None = None
        description: str | None = None
    
    class Schema(GenericSchema, BasicSchema):
        display_url: str | None = None
        base_choices: dict | None = None
        extra_choices: list[list] | None = None
        order_alphabetically: bool | None = None
        choices_count: int | None = None
    
    class SchemaIn(BaseModel):
        name: str = 'placeholder_custom_field_choice'
        description: str | None = None
        base_choices: dict | None = None
        extra_choices: list[list] = [['placeholder_choice', 'Placeholder Choice Value']]
        order_alphabetically: bool | None = None
    
    SchemaList = RootModel[List[Schema]]
    
    # NetBox API Endpoint: /extras/custom-field-choices-sets/
    app: str = 'extras'
    name: str = 'custom_field_choice_sets'
    
    # Schema for CustomFieldChoice objects
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    
    # Unique constraints for CustomFieldChoice objects
    unique_together = ['name']
    required_fields = ['name']
    
    # API
    prefix = '/custom_field_choice'
    api_router = APIRouter(tags=['Extras / Custom Field Choices'])
    

class CustomField(NetBoxBase):
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str  | None = None
        name: str | None = None
        description: str | None = None
    
    class Schema(GenericSchema, BasicSchema):
        display_url: str | None = None
        object_types: List[str] | None = None
        type: NetBoxBase.ValueLabelSchema | None = None
        related_object_type: Optional[Union[Any, None]] | None = None
        data_type: str | None = None
        name: str | None = None
        label: str | None = None
        group_name: str | None = None
        description: str | None = None
        required: bool | None = None
        unique: bool | None = None
        search_weight: int | None = None
        filter_logic: NetBoxBase.ValueLabelSchema | None = None
        ui_visible: NetBoxBase.ValueLabelSchema | None = None
        ui_editable: NetBoxBase.ValueLabelSchema | None = None
        is_cloneable: bool | None = None
        default: dict | None = None
        related_object_filter: Optional[Union[Any, None]] | None = None
        weight: int | None = None
        validation_minimum: int | None = None
        validation_maximum: int | None = None
        validation_regex: str | None = None
        choice_set: CustomFieldChoice.BasicSchema | None = None
        comments: str | None = None
        created: str | None = None
        last_updated: str | None = None

    class SchemaIn(BaseModel):
        object_types: List[str] = ['dcim.device']
        name: str = 'placeholder_custom_field'
        label: str | None = None
        group_name: str | None = None
        description: str = 'Placeholder Custom Field'
        type: str = 'text'
        required: bool = False
        unique: bool = False
        default: dict | None = None
        validation_regex: str | None = None
        validation_minimum: int | None = None
        validation_maximum: int | None = None
        search_weight: int = 1000
        filter_logic: str = 'loose'
        ui_visible: str = 'hidden'
        ui_editable: str = 'hidden'
        weight: int = 100
        is_cloneable: bool | None = None
        choice_set: CustomFieldChoice.BasicSchema | None = None
        comments: str | None = None
    
    SchemaList = RootModel[List[Schema]]
    
    # NetBox API Endpoint: /extras/custom-fields/
    app: str = 'extras'
    name: str = 'custom_fields'
    
    # Schema for CustomField objects
    schema = Schema
    schema_in = SchemaIn
    schema_list = SchemaList
    
    # Unique constraints for CustomField objects
    unique_together = ['name']
    required_fields = [
        'object_types', 'name', 'type', 'search_weight',
        'filter_logic', 'ui_visible', 'ui_editable', 'weight'
    ]
    
    # API
    prefix = '/custom_field'
    api_router = APIRouter(tags=['Extras / Custom Fields'])
        
        

        
        
        
        
        
        
        
        
