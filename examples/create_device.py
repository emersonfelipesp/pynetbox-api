import pynetbox
from pynetbox_api.session import NetBoxAPI

DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'

netbox_session = pynetbox.api(DEMO_URL)
token = netbox_session.create_token(DEMO_USER_NAME, DEMO_PASSWORD)

nb_api = NetBoxAPI(pynetbox_api=netbox_session)

# Create a manufacturer
device = nb_api.dcim.devices(
    name='Creating a device',
    slug='creating-a-device',
    description='This is a test device',
)

print(f'nb_api.dcim.devices.bootstrap_placeholder: {nb_api.dcim.devices.bootstrap_placeholder}')

print(nb_api.dcim.devices.update)

print('\nTeste: ', device)
print(device.json)

print(device.id)
print(device.json.get('name'))