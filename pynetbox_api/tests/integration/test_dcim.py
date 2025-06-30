import pynetbox

from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.dcim.device_type import DeviceType
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
@pytest.mark.parametrize("id", range(3))
def test_create_manufacturer(pynetbox_demo_session, id):
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
    
@pytest.mark.integration
def test_create_placeholder_device_type(pynetbox_demo_session):
    device_type_placeholder = DeviceType(bootstrap_placeholder=True, nb=pynetbox_demo_session)
    
    assert getattr(device_type_placeholder, 'nb') is not None
    
    print('device_type_placeholder', device_type_placeholder.nb)
    assert device_type_placeholder.result is not None
    assert device_type_placeholder.id is not None
    
    assert dict(device_type_placeholder) is not None
    assert dict(device_type_placeholder) == device_type_placeholder.result
    
    assert dict(device_type_placeholder).get('model') == DeviceType.SchemaIn.model_fields.get('model').default
    assert dict(device_type_placeholder).get('slug') == DeviceType.SchemaIn.model_fields.get('slug').default
    assert dict(device_type_placeholder).get('description') == DeviceType.SchemaIn.model_fields.get('description').default


@pytest.mark.integration
@pytest.mark.dependency(name='test_create_device_type')
@pytest.mark.parametrize("id", range(3))
def test_create_device_type(pynetbox_demo_session, id):
    device_type_model = f"Integration Test Device Type {id}"
    device_type_slug = f"integration-test-device-type-{id}"
    device_type_description = "This is a test device type for integration tests"
    
    device_type = DeviceType(
        nb=pynetbox_demo_session,
        manufacturer=Manufacturer(bootstrap_placeholder=True, nb=pynetbox_demo_session).id,
        model=device_type_model,
        slug=device_type_slug,
        description=device_type_description
    )
    
    assert device_type.result is not None
    assert device_type.id is not None
    
    assert dict(device_type) is not None
    
    dict_device_type: dict = dict(device_type)
    assert dict_device_type == device_type.result
    
    assert dict_device_type.get('model') == device_type_model
    assert dict_device_type.get('slug') == device_type_slug
    assert dict_device_type.get('description') == device_type_description



'''
device_new = Device(
    name="Test Device"
)
print('\ndevice_new.result: ', device_new.result)
print('\ndict(device_new): ', dict(device_new))
'''








