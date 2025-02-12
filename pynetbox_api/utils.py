from pydantic import BaseModel
from typing import List, Any, Optional, Union
from pynetbox_api.extras import TagsBasicSchema

class ValueLabelSchema(BaseModel):
    value: str | None = None
    label: Optional[Union[Any, str, int, None]] = None

class StatusSchema(BaseModel):
    value: str | None = None
    label: str | None = None

class GenericSchema(BaseModel):
    tags: List[TagsBasicSchema] = []
    custom_fields: dict[str, str | None] = {}
    created: str | None = None
    last_updated: str | None = None
