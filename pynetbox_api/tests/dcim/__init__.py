from typing import List
from pydantic import Field

from pynetbox_api.tests import TestNetBoxBase
from pynetbox_api.dcim.site import Site
from pynetbox_api.extras.tag import Tags

class TestTag(Tags):
    nb = TestNetBoxBase.nb
    
class TestSite(Site):
    nb = TestNetBoxBase.nb
    
    class SchemaIn(Site.SchemaIn):
        tags: List[int] = Field(default_factory=lambda: [TestTag(bootstrap_placeholder=True).id], exclude=True)

    schema_in = SchemaIn

site = TestSite(bootstrap_placeholder=True)
print(site.result)



