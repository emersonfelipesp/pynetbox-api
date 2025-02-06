from pydantic import BaseModel, RootModel
from typing import List

from pynetbox_api.schemas.extras import TagsSchema

class ManufacturerSchema(BaseModel):
    id: int | None = None
    url: str | None = None
    display: str | None = None
    display_url: str | None = None
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    tags: List[TagsSchema] | None = None
    custom_fields: dict | None = None
    created: str | None = None
    last_updated: str | None = None