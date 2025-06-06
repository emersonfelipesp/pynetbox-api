import pynetbox
from pynetbox_api.session import establish_netbox_session
from pynetbox_api.database import NetBoxEndpoint

import requests
from bs4 import BeautifulSoup

DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'
DEMO_TOKEN: str = '4aba5565210cea968a3c47e49c39b0fed8602742'

example_status_response = {
    'django-version': '5.2.1', 
    'installed-apps': {
        'django_filters': '25.1',
        'django_prometheus': '2.3.1',
        'django_rq': '3.0.1',
        'django_tables2': '2.7.5',
        'drf_spectacular': '0.28.0',
        'drf_spectacular_sidecar': '2025.5.1',
        'mptt': '0.17.0',
        'rest_framework': '3.16.0',
        'social_django': '5.4.3',
        'taggit': '6.1.0',
        'timezone_field': '7.1'
        }, 
    'netbox-version': '4.3.1', 
    'netbox-full-version': '4.3.1', 
    'plugins': {'netbox_demo': '0.5.0'}, 
    'python-version': '3.12.9', 
    'rq-workers-running': 1
}


def login_to_demo_site() -> requests.Session | None:
    """Performs a web-based login to the NetBox demo site using the demo credentials.

    This function handles CSRF token retrieval and session management for web-based authentication.

    Returns:
        requests.Session | None: A requests session object if login is successful, None otherwise
    """
    login_url = 'https://demo.netbox.dev/plugins/demo/login/'
    session = requests.Session()

    # Get the login page to retrieve the CSRF token
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

    # Prepare login data
    login_data = {
        'username': DEMO_USER_NAME,
        'password': DEMO_PASSWORD,
        'csrfmiddlewaretoken': csrf_token
    }

    # Perform login
    headers = {
        'Referer': login_url
    }
    login_response = session.post(login_url, data=login_data, headers=headers)
    print(login_response.text)
    # Check if login was successful
    if login_response.ok and 'Log out' in login_response.text:
        print("Login successful")
        return session
    else:
        print("Login failed")
        return None


def create_test_user() -> dict | None:
    """Creates a test user on the NetBox demo instance.
    
    This function requires successful login to the demo site first.
    https://demo.netbox.dev/plugins/demo/login/

    Returns:
        dict | None: User information if creation is successful, None otherwise

    Raises:
        Exception: If login fails
    """
    login_to_demo_site()
    if login_to_demo_site() is None:
        raise Exception('Login failed')
    else:
        create_test_user()

netbox_endpoint = NetBoxEndpoint(
    name='Demo NetBox',
    ip_address='159.65.38.255',
    domain='demo.netbox.dev',
    port=443,
    token='4aba5565210cea968a3c47e49c39b0fed8602742',
)

def test_session(nb: pynetbox.api) -> dict | None:
    """Tests the NetBox API session by attempting to retrieve the system status.

    This function implements a robust error handling mechanism:
    1. Attempts to get system status with existing token
    2. If token is invalid:
       - Tries to create a new token
       - If username/password is invalid, attempts web login
       - Retries status check with new token
    3. Raises exceptions for other errors

    Args:
        nb (pynetbox.api): A pynetbox API session object (defaults to a new session)

    Returns:
        dict | None: System status information if successful, None otherwise
    """
    if not nb:
        return None
    
    try:
        return nb.status()
    except pynetbox.core.query.RequestError as e:
        if '403 Forbidden' and 'Invalid token' in str(e):
            try:
                # Try to create a new token only if the existing one is invalid
                token = nb.create_token(DEMO_USER_NAME, DEMO_PASSWORD)
                # Update the session with the new token
                nb.token = token.key
                return nb.status()
            except pynetbox.core.query.RequestError as e:
                try:
                    if 'Invalid username/password' in str(e):
                        print(f'Invalid username/password: {e}')
                        login_to_demo_site()
                        
                        token = nb.create_token(DEMO_USER_NAME, DEMO_PASSWORD)
                        # Update the session with the new token
                        nb.token = token.key
                        return nb.status()
                    else:
                        print(f'Error to create token: {e}')
                        raise e
                except Exception as e:
                    print(f'Error to create token: {e}')
                    raise e
                
            except Exception as e:
                print(f'Error to get status: {e}')
                raise e
    
demo_netbox_session = establish_netbox_session(netbox_endpoint)
test_demo_netbox_session = test_session(demo_netbox_session)

print(test_demo_netbox_session)


