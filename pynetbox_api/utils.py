from pydantic import BaseModel
from typing import List
from pynetbox_api.extras import TagsSchema

class ValueLabelSchema(BaseModel):
    value: str | None = None
    label: str | None = None

class StatusSchema(BaseModel):
    value: str | None = None
    label: str | None = None
    
class GenericSchema(BaseModel):
    tags: List[TagsSchema] = []
    custom_fields: dict[str, str | None] = {}
    created: str | None = None
    last_updated: str | None = None
