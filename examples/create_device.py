import pynetbox
from pynetbox_api.session import NetBoxAPI

DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'

netbox_session = pynetbox.api(DEMO_URL)
token = netbox_session.create_token(DEMO_USER_NAME, DEMO_PASSWORD)

nb_api = NetBoxAPI(pynetbox_api=netbox_session)

# Create a manufacturer
device = nb_api.dcim.device(
    name='Creating a device',
    slug='creating-a-device',
    description='This is a test device',
)

print(nb_api.dcim.device.update)

print('\nTeste: ', device)
print(device.json)