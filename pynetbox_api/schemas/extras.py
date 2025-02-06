from pydantic import BaseModel, RootModel     
from typing import List

class TagsSchema(BaseModel):
    id: int
    url: str | None = None
    display_url: str | None = None
    name: str
    slug: str
    color: str | None = None