
from pydantic import BaseModel
from typing import List
from pynetbox_api.extras.tag import Tags

class GenericSchema(BaseModel):
    tags: List[Tags.BasicSchema] = []
    custom_fields: dict[str, str | None] = {}
    created: str | None = None
    last_updated: str | None = None