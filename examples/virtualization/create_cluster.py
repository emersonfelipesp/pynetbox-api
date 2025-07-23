import pynetbox
from pynetbox_api.session import NetBoxAPI

DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'

netbox_session = pynetbox.api(DEMO_URL)
token = netbox_session.create_token(DEMO_USER_NAME, DEMO_PASSWORD)

nb_api = NetBoxAPI(pynetbox_api=netbox_session)

# Create a cluster
cluster = nb_api.virtualization.clusters(
    name='Creating a cluster',
    slug='creating-a-cluster',
    description='This is a test cluster',
    type=1
)

cluster_2 = nb_api.virtualization.clusters(
    name='Creating a cluster 2',
    slug='creating-a-cluster-2',
    description='This is a test cluster 2',
    type=1
)

create_a_cluster = nb_api.virtualization.clusters(
    name='Creating a cluster 3',
    slug='creating-a-cluster-3',
    description='This is a test cluster 3',
)

print(cluster_2)

print(f'nb_api.virtualization.clusters.bootstrap_placeholder: {nb_api.virtualization.clusters.bootstrap_placeholder}')

print(nb_api.virtualization.clusters.update)

print('\nTeste: ', cluster)
print(cluster.json)

print(cluster.id)
print(cluster.json.get('name'))