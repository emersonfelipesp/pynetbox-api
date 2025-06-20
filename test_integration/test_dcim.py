import pynetbox

from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.dcim.device import Device
from pynetbox_api.session import NetBoxBase

NetBoxBase.nb = pynetbox.api("https://demo.netbox.dev", token="a86e30c4eabfb99aa2ad3c016c0b4fb792ee5332")


def test_create_placeholder_manufacturer():
    manufacturer_placeholder = Manufacturer(bootstrap_placeholder=True)
    assert manufacturer_placeholder.result is not None
    assert manufacturer_placeholder.id is not None
    
    assert dict(manufacturer_placeholder) is not None
    assert dict(manufacturer_placeholder) == manufacturer_placeholder.result
    
    assert dict(manufacturer_placeholder).get('name') == Manufacturer.SchemaIn.model_fields.get('name').default
    assert dict(manufacturer_placeholder).get('slug') == Manufacturer.SchemaIn.model_fields.get('slug').default
    assert dict(manufacturer_placeholder).get('description') == Manufacturer.SchemaIn.model_fields.get('description').default
    
    
    
def test_create_manufacturer():
    for id in range(3):
        manufacturer_name = f"Integration Test Manufacturer {id}"
        manufacturer_slug = f"integration-test-manufacturer-{id}"
        manufacturer_description = "This is a test manufacturer for integration tests"
        
        manufacturer = Manufacturer(
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


def test_delete_manufacturer():
    #
    # Create a new manufacturer to be deleted
    #
    manufacturer_name = "Integration Test Delete Manufacturer"
    manufacturer_slug = "integration-test-delete-manufacturer"
    manufacturer_description = "This is a test manufacturer for integration tests to be deleted"
    
    manufacturer = Manufacturer(
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


def test_get_by_id_manufacturer():
    manufacturer = Manufacturer()
    get_manufacturer = manufacturer.get(id=1)
    
    assert manufacturer.result is not None
    assert manufacturer.id is not None
    assert manufacturer.json is not None
    
    assert manufacturer.json.get('id') == 1


def test_get_by_name_manufacturer():
    manufacturer = Manufacturer()
    get_manufacturer = manufacturer.get(name='Integration Test Manufacturer')
    
    assert manufacturer.result is not None
    assert manufacturer.id is not None
    assert manufacturer.json is not None
    
    assert manufacturer.result.get('name') == 'Integration Test Manufacturer'
    





'''
device_new = Device(
    name="Test Device"
)
print('\ndevice_new.result: ', device_new.result)
print('\ndict(device_new): ', dict(device_new))
'''








