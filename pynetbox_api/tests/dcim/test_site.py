
'''from typing import List
from pydantic import Field

from pynetbox_api.tests import TestNetBoxBase
from pynetbox_api.dcim.site import Site
from pynetbox_api.extras.tag import Tags

class TestTag(Tags):
    """
    TestTag is a subclass of Tags that is used to test the Site model.
    """
    nb = TestNetBoxBase.nb


def test_tag_create():
    tag = TestTag(bootstrap_placeholder=True)
    
    assert tag is not None
    assert tag.result is not None
    assert tag.id is not None
    
    pynetbox_tag = tag.nb.extras.tags.get(id=tag.id)
    
    assert pynetbox_tag is not None
    
    assert tag.result.get('name') == pynetbox_tag.name
    assert tag.result.get('slug') == pynetbox_tag.slug
    

class TestSite(Site):
    nb = TestNetBoxBase.nb
    
    class SchemaIn(Site.SchemaIn):
        tags: List[int] = Field(default_factory=lambda: [TestTag(bootstrap_placeholder=True).id], exclude=True)

    schema_in = SchemaIn


def test_site_create():
    site = TestSite(bootstrap_placeholder=True)
    
    assert site is not None
    assert site.result is not None
    assert site.id is not None
    
    pynetbox_site = site.nb.dcim.sites.get(id=site.id)
    
    assert pynetbox_site is not None
    
    assert site.result.get('name') == pynetbox_site.name
    assert site.result.get('slug') == pynetbox_site.slug
'''
    


