import pynetbox
from pynetbox_api.dcim.manufacturer import Manufacturer
from pynetbox_api.session import NetBoxBase

DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'

netbox_session = pynetbox.api(DEMO_URL)
token = netbox_session.create_token(DEMO_USER_NAME, DEMO_PASSWORD)

# Configure the NetBox session
NetBoxBase.nb = netbox_session

# Create a manufacturer
manufacturer = Manufacturer(
    name='Creating a manufacturer',
    slug='creating-a-manufacturer',
    description='This is a test manufacturer',
)

print('\nTeste: ', manufacturer)
print(manufacturer.json)