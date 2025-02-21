
from pydantic import BaseModel
from typing import List, Optional, Union, Any
from pynetbox_api.extras.tag import Tags

class GenericSchema(BaseModel):
    tags: List[Tags.BasicSchema] = []
    custom_fields: dict[str, Optional[Union[str, int, Any]] | None] = {}
    created: str | None = None
    last_updated: str | None = None