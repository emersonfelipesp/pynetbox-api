from pynetbox_api.session import NetBoxBase
from pynetbox_api.schemas.extras import (
    TagsSchema,
    TagsSchemaIn,
    TagsSchemaList
)

class Tags(NetBoxBase):
    app = 'extras'
    name = 'tags'
    schema = TagsSchema
    schema_in = TagsSchemaIn
    schema_list = TagsSchemaList
    unique_together = ['name', 'slug']