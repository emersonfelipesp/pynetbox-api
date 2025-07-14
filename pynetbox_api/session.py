import warnings

import requests
from sqlalchemy.util import bool_or_str
import urllib3
import pynetbox

# json and hashlib are used to uniquely identify the objects in the cache
import json
import hashlib

from typing import (
    Any,
    Annotated,
    Dict,
    List,
)

from typing_extensions import Doc
from pydantic import BaseModel, RootModel
from typing import List, Any, Optional, Union

from fastapi import Query
from fastapi.responses import JSONResponse
from pynetbox_api.exceptions import FastAPIException
from pynetbox_api.cache import global_cache

#
# Database connection imports
#
from sqlmodel import select
from pynetbox_api.base import NetBoxBase
from pynetbox_api.objects import DcimObjects


# Global variables for NetBox connection
NETBOX_URL = "https://netbox.example.com"
NETBOX_TOKEN = "provide-your-token"
NETBOX_STATUS: bool = False
NETBOX_SESSION = None  # Global session variable

class NetBoxAPI:
    
    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        threading: bool = False,
        strict_filters: bool = False,
        pynetbox_api: pynetbox.api | None = None
    ):
        self.url = url
        self.token = token
        self.threading = threading
        self.strict_filters = strict_filters
        
        if pynetbox_api:
            self.session = pynetbox_api
        else:
            self.session = pynetbox.api(
                url=url,
                token=token,
                threading=threading
            )
        
        self.dcim = DcimObjects(api=self)
        
''' 
def get_netbox_endpoint() -> NetBoxEndpoint | None:
    try:
        # Get the database session
        database_session = next(get_session())
        
        # Get the first NetBox endpoint from the database
        netbox_endpoint = database_session.exec(select(NetBoxEndpoint)).first()
        
        # Return the NetBox endpoint
        return netbox_endpoint

    except OperationalError as error:
        print('Table does not exist, creating it...')
        create_db_and_tables()
        
        # Try again
        return get_netbox_endpoint()

def establish_netbox_session(netbox_endpoint: NetBoxEndpoint) -> pynetbox.api | None:
    warnings.warn(
        f"establish_netbox_session is deprecated; use NetBoxAPI class instead",
        category=DeprecationWarning,
        stacklevel=2
    )
    global NETBOX_SESSION, NETBOX_STATUS
    
    if not netbox_endpoint:
        return None
    
    # If we already have a working session, return it
    if NETBOX_SESSION and NETBOX_STATUS:
        return NETBOX_SESSION
        

    print(f'Found NetBox endpoint: {netbox_endpoint.name}')
    urllib3.disable_warnings()

    # Try different connection strategies
    connection_strategies = [
        # Strategy 1: Use configured URL with SSL verification
        {
            'url': netbox_endpoint.url,
            'verify': netbox_endpoint.verify_ssl,
            'description': 'configured URL with SSL verification'
        },
        # Strategy 2: Use configured URL without SSL verification
        {
            'url': netbox_endpoint.url,
            'verify': False,
            'description': 'configured URL without SSL verification'
        },
        # Strategy 3: Try HTTP if HTTPS fails
        {
            'url': f"http://{netbox_endpoint.ip_address.split('/')[0]}:{netbox_endpoint.port}",
            'verify': False,
            'description': 'HTTP fallback'
        },
        # Strategy 4: Try localhost
        {
            'url': f"http://localhost:{netbox_endpoint.port}",
            'verify': False,
            'description': 'localhost fallback'
        }
    ]

    for strategy in connection_strategies:
        try:
            print(f'🔄 Attempting connection using {strategy["description"]}...')
            session = requests.Session()
            session.verify = strategy['verify']
            
            NETBOX_SESSION = pynetbox.api(
                strategy['url'],
                token=netbox_endpoint.token,
            )
            NETBOX_SESSION.http_session = session
            
            # Test the connection
            print('🔍 Testing connection with status check...')
            NETBOX_SESSION.status()
            print('✅ Status check successful')
            NETBOX_STATUS = True
            return NETBOX_SESSION
            
        except Exception as error:
            print(f"❌ Connection attempt with {strategy['url']} failed: {str(error)}")
            NETBOX_STATUS = False
            NETBOX_SESSION = None
            continue
    
    print('🚫 All connection attempts failed')
    return None

    
netbox_endpoint = get_netbox_endpoint()
RawNetBoxSession = establish_netbox_session(netbox_endpoint=netbox_endpoint) if netbox_endpoint else None
'''
# Export NetBoxBase for backward compatibility
__all__ = ['NetBoxAPI']

