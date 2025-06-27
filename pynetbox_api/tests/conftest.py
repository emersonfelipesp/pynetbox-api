import pytest

from pynetbox_api.session import NetBoxBase
from pynetbox_api.tests.integration.test_session import establish_demo_session

@pytest.fixture(scope='session', autouse=True)
def pynetbox_demo_session():
    '''
    This fixture is used to set the NetBoxBase.nb attribute to the demo session.
    This is used to avoid having to pass the NetBoxBase.nb attribute to each test function.
    '''
    print("\n🔧 Setting up pynetbox_demo_session fixture...")
    session = establish_demo_session()
    
    try:
        # This is a test to check if the session is valid
        session.status()
    except Exception as e:
        error_msg: str = f"❌ Error setting up pynetbox_demo_session fixture: {e}"
        print(error_msg)
        pytest.exit(error_msg, returncode=1)
    
    yield session

