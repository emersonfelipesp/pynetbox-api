import pynetbox
from pynetbox_api.session import establish_netbox_session
from pynetbox_api.database import NetBoxEndpoint
from pynetbox_api.session import NetBoxBase

import requests
from bs4 import BeautifulSoup

DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'
LOGIN_SUCCESSFUL: bool = False

demo_config = {
    'url': DEMO_URL,
    'username': DEMO_USER_NAME,
    'password': DEMO_PASSWORD,
    'token': None,
}

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


# This function, `login_to_demo_site`, attempts to log into the NetBox demo site using predefined credentials.
# It can retry the login process once if the initial attempt fails.
def login_to_demo(mode: str = 'login', already_retried: bool = False) -> bool:
    """Performs a web-based login to the NetBox demo site using the demo credentials.

    This function handles CSRF token retrieval and session management for web-based authentication.

    Returns:
        requests.Session | None: A requests session object if login is successful, None otherwise
    """
    global LOGIN_SUCCESSFUL
    if LOGIN_SUCCESSFUL:
        return True
    
    login_url = ''
    
    if mode == 'login':
        login_url = 'https://demo.netbox.dev/login/'
    elif mode == 'create_user':
        login_url = 'https://demo.netbox.dev/plugins/demo/login/'
    else:
        raise ValueError(f'Invalid mode: {mode}')
    
    #print(login_url)
    # Create a new session object to manage cookies and headers.
    session = requests.Session()

    # Send a GET request to the login page to retrieve the HTML content.
    response = session.get(login_url)
    
    # Parse the HTML content using BeautifulSoup to extract the CSRF token.
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

    # Prepare the login data including the username, password, and CSRF token.
    login_data = {
        'username': DEMO_USER_NAME,
        'password': DEMO_PASSWORD,
        'csrfmiddlewaretoken': csrf_token
    }

    # Set the headers for the POST request, including the Referer to the login URL.
    headers = {
        'Referer': login_url
    }
    
    # Send a POST request to the login URL with the login data and headers to attempt login.
    login_response = session.post(login_url, data=login_data, headers=headers)
    
    # If the login failed due to a incorrect username or password, try to create a new user.
    if 'Please enter a correct username and password' in login_response.text:
        login_session = login_to_demo(mode='create_user')
        if login_session:
            return login_session
        else:
            return None
        
    #print(login_response.text)
    # Check if the login failed due to a duplicate user.
    if 'duplicate key value' in login_response.text or 'already exists' in login_response.text:
        print("Login failed. User already exists.")
        return False
    
    # Check if the login was successful by verifying the response status
    if login_response.ok:
        # If successful, print a success message and return the session object.
        print("Login successful")
        LOGIN_SUCCESSFUL = True
        return True
    else:
        # If login failed, print a failure message.
        print("Login failed")
        # If retry is allowed, return None to indicate failure.
        if already_retried:
            return False
        else:
            print("Retrying login...")
            # Otherwise, retry the login process once by calling the function recursively with retry set to True.
            return login_to_demo(already_retried=True)
    
    return False



netbox_endpoint = NetBoxEndpoint(
    name='Demo NetBox',
    ip_address='159.65.38.255',
    domain='demo.netbox.dev',
    port=443,
    token='4aba5565210cea968a3c47e49c39b0fed8602742',
)

'''
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
'''


def establish_demo_session() -> pynetbox.api | None:
    if login_to_demo() is False:
        raise Exception('Login failed')
    
    # If the token is not set, create a new token
    if demo_config.get('token') is None:
        # pynetbox API object (session)
        nb = pynetbox.api(demo_config.get('url'))
    
        demo_config['token'] = nb.create_token(
            demo_config['username'],
            demo_config['password']
        )
        
    else:
        nb = pynetbox.api(demo_config.get('url'), token=demo_config.get('token'))
        
    return nb


class TestNetBoxBase(NetBoxBase):
    """
    Test-specific version of NetBoxBase that uses a separate NetBox session.
    This allows test code to use a different NetBox connection without affecting
    the main NetBoxBase class.
    """
    nb: pynetbox.api = establish_demo_session()

def test_login_to_demo():
    assert login_to_demo() is True


def test_establish_demo_session():
    pynetbox_session = TestNetBoxBase.nb
    
    assert pynetbox_session is not None
    assert pynetbox_session.version is not None
    assert pynetbox_session.dcim.devices.count() is not None and pynetbox_session.dcim.devices.count() > 0
    
    assert isinstance(pynetbox_session, pynetbox.api)
    
    pynetbox_status = pynetbox_session.status()
    assert pynetbox_status is not None
    assert pynetbox_status.get('django-version') is not None
    assert pynetbox_status.get('netbox-version') is not None
    assert pynetbox_status.get('netbox-full-version') is not None

    
    

