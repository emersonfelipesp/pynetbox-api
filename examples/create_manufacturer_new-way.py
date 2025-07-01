import pynetbox
from pynetbox_api.session import NetBoxAPI

DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'

netbox_session = pynetbox.api(DEMO_URL)
token = netbox_session.create_token(DEMO_USER_NAME, DEMO_PASSWORD)

nb_api = NetBoxAPI(pynetbox_api=netbox_session)

# Create a manufacturer
manufacturer = nb_api.dcim.manufacturer(
    name='Creating a manufacturer',
    slug='creating-a-manufacturer',
    description='This is a test manufacturer',
)

print(nb_api.dcim.manufacturer.update)

print('\nTeste: ', manufacturer)
print(manufacturer.json)