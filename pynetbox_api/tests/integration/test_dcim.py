import pynetbox

from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.dcim.device import Device
from pynetbox_api.session import NetBoxBase

import pytest

@pytest.mark.integration
def test_fixture_is_working(pynetbox_demo_session):
    """Test to verify that the pynetbox_demo_session fixture is working"""
    print(f"\n🔍 Checking if NetBoxBase.nb is set: {pynetbox_demo_session}")
    assert pynetbox_demo_session is not None
    print("✅ NetBoxBase.nb is properly set by the fixture!")

@pytest.mark.integration
def test_create_placeholder_manufacturer(pynetbox_demo_session):
    manufacturer_placeholder = Manufacturer(bootstrap_placeholder=True, nb=pynetbox_demo_session)
    
    assert getattr(manufacturer_placeholder, 'nb') is not None
    
    print('manufacturer_placeholder', manufacturer_placeholder.nb)
    assert manufacturer_placeholder.result is not None
    assert manufacturer_placeholder.id is not None
    
    assert dict(manufacturer_placeholder) is not None
    assert dict(manufacturer_placeholder) == manufacturer_placeholder.result
    
    assert dict(manufacturer_placeholder).get('name') == Manufacturer.SchemaIn.model_fields.get('name').default
    assert dict(manufacturer_placeholder).get('slug') == Manufacturer.SchemaIn.model_fields.get('slug').default
    assert dict(manufacturer_placeholder).get('description') == Manufacturer.SchemaIn.model_fields.get('description').default
  
@pytest.mark.integration
@pytest.mark.dependency(name='test_create_manufacturer')
def test_create_manufacturer(pynetbox_demo_session):
    for id in range(3):
        manufacturer_name = f"Integration Test Manufacturer {id}"
        manufacturer_slug = f"integration-test-manufacturer-{id}"
        manufacturer_description = "This is a test manufacturer for integration tests"
        
        manufacturer = Manufacturer(
            nb=pynetbox_demo_session,
            name=manufacturer_name,
            slug=manufacturer_slug,
            description=manufacturer_description
        )
        
        assert manufacturer.result is not None
        assert manufacturer.id is not None
        
        assert dict(manufacturer) is not None
        
        dict_manufacturer: dict = dict(manufacturer)
        assert dict_manufacturer == manufacturer.result
        
        assert dict_manufacturer.get('name') == manufacturer_name
        assert dict_manufacturer.get('slug') == manufacturer_slug
        assert dict_manufacturer.get('description') == manufacturer_description


@pytest.mark.integration
def test_delete_manufacturer(pynetbox_demo_session):
    #
    # Create a new manufacturer to be deleted
    #
    manufacturer_name = "Integration Test Delete Manufacturer"
    manufacturer_slug = "integration-test-delete-manufacturer"
    manufacturer_description = "This is a test manufacturer for integration tests to be deleted"
    
    manufacturer = Manufacturer(
        nb=pynetbox_demo_session,
        name=manufacturer_name,
        slug=manufacturer_slug,
        description=manufacturer_description
    )
    
    assert manufacturer.result is not None
    assert manufacturer.id is not None
    
    
    
    assert dict(manufacturer) is not None
    
    dict_manufacturer: dict = dict(manufacturer)
    assert dict_manufacturer == manufacturer.result
    
    assert dict_manufacturer.get('name') == manufacturer_name
    assert dict_manufacturer.get('slug') == manufacturer_slug
    assert dict_manufacturer.get('description') == manufacturer_description
    
    #
    # Delete the manufacturer
    #
    deleted_manufacturer = manufacturer.delete()
    
    # Check if the manufacturer was deleted
    assert deleted_manufacturer is True
    assert manufacturer.id is None


@pytest.mark.integration
def test_get_by_id_manufacturer(pynetbox_demo_session):
    manufacturer = Manufacturer(nb=pynetbox_demo_session)
    get_manufacturer = manufacturer.get(id=1)
    
    assert manufacturer.result is not None
    assert manufacturer.id is not None
    assert manufacturer.json is not None
    
    assert manufacturer.json.get('id') == 1

@pytest.mark.integration
@pytest.mark.dependency(name='test_get_by_name_manufacturer', depends=['test_create_manufacturer'])
def test_get_by_name_manufacturer(pynetbox_demo_session):
    #
    # Get a manufacturer by name
    # This test depends on the 'test_create_manufacturer' test
    #
    manufacturer = Manufacturer(nb=pynetbox_demo_session)
    manufacturer_name = 'Integration Test Manufacturer 0'
    
    manufacturer.get(name=manufacturer_name)
    
    assert manufacturer.result is not None
    assert manufacturer.id is not None
    assert manufacturer.json is not None
    
    assert manufacturer.result.get('name') == manufacturer_name
        





'''
device_new = Device(
    name="Test Device"
)
print('\ndevice_new.result: ', device_new.result)
print('\ndict(device_new): ', dict(device_new))
'''








