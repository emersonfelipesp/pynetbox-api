# Integration Test Fixture Documentation

## Overview

The integration test module uses a pytest fixture to ensure all tests run against a controlled demo NetBox environment. This documentation explains the fixture's purpose, implementation, and usage.

## Pytest Marks

### Available Marks
- `@pytest.mark.integration`: Marks tests as integration tests
- `@pytest.mark.unit`: Marks tests as unit tests (applied automatically)
- `@pytest.mark.slow`: Marks tests as slow running tests

### Running Tests by Type
```bash
# Run only integration tests
pytest -m integration

# Run only unit tests
pytest -m unit

# Run all tests except integration tests
pytest -m "not integration"

# Run all tests except slow tests
pytest -m "not slow"

# Run integration tests but skip slow ones
pytest -m "integration and not slow"
```

## The `pynetbox_demo_session` Fixture

### Location
```python
# pynetbox_api/tests/integration/__init__.py
```

### Implementation
```python
import pytest
from pynetbox_api.session import NetBoxBase
from pynetbox_api.tests.integration.test_session import establish_demo_session

@pytest.fixture(autouse=True)
def pynetbox_demo_session(monkeypatch):
    monkeypatch.setattr(NetBoxBase, 'nb', establish_demo_session())
    yield
```

## How It Works

### 1. **Autouse Fixture**
- The `autouse=True` parameter means this fixture automatically runs for **every test** in the integration module
- No need to explicitly reference the fixture in test functions
- Ensures consistent test environment across all integration tests

### 2. **Monkeypatching**
- Uses pytest's `monkeypatch` fixture to modify the `NetBoxBase` class
- Replaces the `nb` class attribute with a demo session
- Affects all instances of `NetBoxBase` and its subclasses
- **Important**: The `NetBoxBase.__init__` method checks for a provided `nb` parameter first, then falls back to the class-level `nb` attribute

### 3. **Demo Session Establishment**
- Calls `establish_demo_session()` to create a connection to the NetBox demo site
- Demo site: `https://demo.netbox.dev/`
- Uses predefined demo credentials for authentication

## How the Fixture Works with NetBoxBase

### Class vs Instance Attributes
```python
# Class attribute (set by fixture)
NetBoxBase.nb = demo_session

# Instance attribute (set in __init__)
def __init__(self, nb=None, ...):
    if nb:
        self.nb = nb  # Use provided session
    else:
        self.nb = self.__class__.nb  # Use class-level session (from fixture)
```

### Why This Works
1. **Fixture sets class attribute**: `NetBoxBase.nb = demo_session`
2. **Instance creation**: When `Manufacturer()` is called without `nb` parameter
3. **Fallback mechanism**: `__init__` uses `self.__class__.nb` (the demo session)
4. **Result**: All test instances automatically use the demo session

## Why This Fixture Is Used

### 1. **Test Isolation**
- Prevents tests from affecting production or development NetBox instances
- Ensures tests run in a controlled, predictable environment
- Eliminates risk of data corruption or unintended side effects

### 2. **Consistency**
- All tests use the same NetBox session and environment
- Eliminates environment-specific test failures
- Ensures reproducible test results

### 3. **Demo Environment Benefits**
- Demo site is publicly accessible and designed for testing
- Contains sample data that tests can rely on
- No risk of affecting real infrastructure data

### 4. **Class-Level Modification**
- Since `NetBoxBase.nb` is a class attribute, the modification affects all subclasses
- Models like `Manufacturer`, `Device`, etc. automatically use the demo session
- No need to pass session objects to individual test instances

## Demo Session Details

### Authentication Process
1. **Web Login**: Performs web-based authentication to the demo site
2. **CSRF Token Handling**: Manages CSRF tokens for secure login
3. **Token Creation**: Creates API tokens for programmatic access
4. **Session Management**: Maintains session state across tests

### Demo Configuration
```python
DEMO_URL: str = 'https://demo.netbox.dev/'
DEMO_USER_NAME: str = 'pynetbox_api'
DEMO_PASSWORD: str = '@T3st0nly'
```

### Error Handling
- Retries login on failure
- Handles duplicate user scenarios
- Provides fallback authentication methods

## Impact on Tests

### Before Fixture (Without Demo Session)
```python
# Tests would use whatever NetBox session is configured globally
# Could affect production data or fail due to environment differences
manufacturer = Manufacturer(name="Test Manufacturer")
```

### After Fixture (With Demo Session)
```python
# Tests automatically use the demo session
# Safe, isolated, and consistent environment
manufacturer = Manufacturer(name="Test Manufacturer")
# Uses NetBoxBase.nb = demo_session automatically
```

## Test Examples

All tests in the integration module benefit from this fixture:

```python
# test_dcim.py
@pytest.mark.integration
def test_create_manufacturer():
    manufacturer = Manufacturer(
        name="Integration Test Manufacturer",
        slug="integration-test-manufacturer",
        description="Test manufacturer"
    )
    # Automatically uses demo session via NetBoxBase.nb
    assert manufacturer.result is not None
    assert manufacturer.id is not None
```

## Best Practices

### 1. **Test Cleanup**
- Tests should clean up any data they create
- Demo environment is shared, so tests should be respectful
- Use unique identifiers to avoid conflicts

### 2. **Dependencies**
- Tests can depend on each other using `@pytest.mark.dependency`
- Fixture ensures consistent state between dependent tests

### 3. **Error Handling**
- Tests should handle demo site availability gracefully
- Consider demo site maintenance windows

## Troubleshooting

### Common Issues

1. **Demo Site Unavailable**
   - Check if `https://demo.netbox.dev/` is accessible
   - Verify demo credentials are still valid

2. **Authentication Failures**
   - Demo credentials may have changed
   - Check for rate limiting or IP restrictions

3. **Test Failures**
   - Ensure tests clean up after themselves
   - Check for conflicts with other tests

### Debugging
```python
# To debug the fixture, you can temporarily disable autouse
@pytest.fixture(autouse=False)  # Change to False for debugging
def pynetbox_demo_session(monkeypatch):
    # ... fixture code
```

## Related Files

- `test_session.py`: Contains the `establish_demo_session()` function
- `session.py`: Contains the `NetBoxBase` class definition
- `test_dcim.py`: Example tests using the fixture

## Conclusion

The `pynetbox_demo_session` fixture is essential for maintaining a reliable, isolated, and consistent testing environment. It ensures that all integration tests run against a controlled demo NetBox instance, preventing data corruption and providing predictable test results. 