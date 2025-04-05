import requests
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

NETBOX_URL = "https://netbox.example.com"
NETBOX_TOKEN = "provide-your-token"
NETBOX_STATUS: bool = False

'''
try:
    from pynetbox_api.env import NETBOX_URL, NETBOX_TOKEN
except ImportError as error:
    print('Error to Import environment variables.')
    
def _establish_from_env():
    print('Trying to establish connection to NetBox using env.py file...')
    try:
        if not NETBOX_URL:
            print('NETBOX_URL environment variable not found.',)
        
        if not NETBOX_TOKEN:
            print('NETBOX_TOKEN environment variable not found.',)

        if NETBOX_URL and NETBOX_TOKEN:
            urllib3.disable_warnings()

            session = requests.Session()
            session.verify = False
            
            try:
                nb = pynetbox.api(
                    NETBOX_URL,
                    token=NETBOX_TOKEN,
                )
                nb.http_session = session
                
                return nb
            except Exception as error:
                raise FastAPIException(
                    message=f'Error to connect to Netbox ({NETBOX_URL})',
                    python_exception=str(error)
                )
    except FastAPIException as error:
        print(f'Error to load environment variables.\n{error}')
    except Exception as error:
        print(f'Unexpected error. {error}')
'''

def _establish_from_sql():
    print('Trying to establish connection to NetBox using SQL database...')
    
    from sqlmodel import select
    from pynetbox_api.database import NetBoxEndpoint, get_session
    from sqlalchemy.exc import OperationalError
    
    database_session = next(get_session())
    try:
        netbox_endpoint = database_session.exec(select(NetBoxEndpoint)).first()
    except OperationalError as error:
        # If table does not exist, create it.
        print('Table does not exist, creating it...')
        from pynetbox_api.database import create_db_and_tables
        create_db_and_tables()
        netbox_endpoint = database_session.exec(select(NetBoxEndpoint)).first()
    
    
    
    if netbox_endpoint:
        urllib3.disable_warnings()

        session = requests.Session()
        
        #session.verify = netbox_endpoint.verify_ssl
        session.verify = False
        
        https_url = f'https://{netbox_endpoint.ip_address}:{netbox_endpoint.port}'
        http_url = f'http://{netbox_endpoint.ip_address}:{netbox_endpoint.port}'
        
        url = https_url if netbox_endpoint.verify_ssl else http_url
        try:
            nb = pynetbox.api(
                url,
                token=netbox_endpoint.token,
            )
            nb.http_session = session
            
            return nb
        except Exception as error:
            raise FastAPIException(
                message=f'Error to connect to Netbox ({netbox_endpoint.url})',
                python_exception=str(error)
            )
    
    else:
        print('NetBox Endpoint not found in the database.')
        # If NetBox Endpoint is not found in the database, it will try return the connection from the environment variables
        #return _establish_from_env()
        return None
    
RawNetBoxSession = _establish_from_sql

class NetBoxBase:
    """
    Helper class to interact with NetBox API using pynetbox library.
    
    Attributes:
        use_placeholder: Define is placeholder object will be used to create new objects, filling missing fields.
        bootstrap_placeholder: Define if placeholder object will be created during class instantiation or if no object is provided.
    """
    def __new__(
        cls,
        nb: pynetbox.api = _establish_from_sql(),
        bootstrap_placeholder: bool = False,
        is_bootstrap: bool = False,
        cache: bool = True,
        use_placeholder: bool = True,
        **kwargs
    ):
        if not nb:
            print('NetBox API connection not found.')
            return {}
        
        # Create a new instance of the class
        instance = super().__new__(cls)
        
        # Default values
        instance.nb = nb
        instance.id = 0
        instance.result = {}
    
        try:
            instance.app_name = f'{instance.app}.{instance.name}'
            instance.object = getattr(getattr(nb, instance.app), instance.name)
        except Exception as error:
            raise FastAPIException(
                message=f'Error to get object {instance.app}.{instance.name}',
                detail='__new__ method',
                python_exception=str(error)
            )
        # Check if the NetBox API is reachable
        if not instance.check_status(): return {}
        
        instance.use_placeholder = use_placeholder
        instance.bootstrap_placeholder = bootstrap_placeholder
        
        # Check if the instance is being created with arguments
        if kwargs and not bootstrap_placeholder:
            # Return post method result as the class instance
            result: dict = instance.post(
                json=kwargs,
                cache=cache,
                is_bootstrap=is_bootstrap,
                merge_with_placeholder=use_placeholder
            )

            instance.id = result.get('id', None) if type(result) == dict else None
            instance.id = getattr(result, 'id', None) if type(result) != dict else None
            
            print(result)
            return result if type(result) == dict else result.dict()

        if bootstrap_placeholder:
            instance.placeholder_dict = instance._bootstrap_placeholder()
            #print(f'instance.placeholder_dict: {instance.placeholder_dict}')
            try:
                return instance.post(
                    json=instance.placeholder_dict,
                    cache=cache,
                    is_bootstrap=True,
                    merge_with_placeholder=use_placeholder
                )
                # Return the instance as is if being created with arguments
                
            except FastAPIException as error:
                print(f'Bootstrap placeholder object failed. Error: {error}')
                raise FastAPIException(
                    message=f'Error to create object {instance.app}.{instance.name}',
                    python_exception=str(error)
                )
        
        # Return the instance as is if not being created with arguments
        return instance
        
    def __init__(
        self,
        nb: pynetbox.api = _establish_from_sql(),
        bootstrap_placeholder: Annotated[
            bool,
            Doc(
                """
                Define if placeholder object will be created during class instantiation or if no object is provided.
                If True, it will create a placeholder object using the pydantic schema
                defined in the class as 'schema_in', using the default schema values.
                """
            )
        ] = False,
        use_placeholder: Annotated[
            bool,
            Doc(
                """
                Define is placeholder object will be used to create new objects, filling missing fields.
                It will use the pydantic schema to create the placeholder object.
                The schema is defined in the class as 'schema_in'.
                """
            )
        ] = True,
        **kwargs
    ):
        # Check if the NetBox API is reachable
        self.nb = nb
        self.id = 0
        self.app_name = f'{self.app}.{self.name}'
        self.kwargs = kwargs
        
        if not self.check_status(): return
        
        try:
            self.object = getattr(getattr(nb, self.app), self.name)
        except Exception as error:
            raise FastAPIException(
                message=f'Error to get object {self.app}.{self.name}',
                detail='__new__ method',
                python_exception=str(error)
            )
        
        self.use_placeholder = use_placeholder
        self.bootstrap_placeholder = bootstrap_placeholder
        
        if self.use_placeholder or self.bootstrap_placeholder:
            self.placeholder_dict = self._bootstrap_placeholder()

        if self.bootstrap_placeholder and self.placeholder_dict:
            self.result = self.post(self.placeholder_dict, cache=True, is_bootstrap=True)
            self.id = None
            try:
                self.id = self.result.get('id', None)
            except:
                self.id = getattr(self.result, 'id', None)

    def check_status(self) -> bool:
        global NETBOX_STATUS
        base_message: str = 'Unexpected error to connect to NetBox API using check_status() method.'
        try:
            if NETBOX_STATUS == False:
                print('Trying to get NetBox API status...')
                self.nb.status()
                print('NetBox API status received successfully.')
                NETBOX_STATUS = True
                return NETBOX_STATUS
            else:
                return NETBOX_STATUS
        except pynetbox.core.query.ContentError:
            print(f'Error to connect to NetBox API. The API URL is invalid.\n{error}')
            NETBOX_STATUS = False
        except pynetbox.RequestError as error:
            print(f'Error to connect to NetBox API.\nError: {error}')
            NETBOX_STATUS = False
        except requests.exceptions.SSLError as error:
            # Error: HTTPSConnectionPool(host='10.0.30.200', port=443): Max retries exceeded with url: /api/status/
            # (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1000)')))
            # This error happens when the certificate is self-signed.
            # The "solution" is to disable the SSL verification.
            print(f'SSL Error trying to connect to NetBox API.\nError: {error}')
            self.nb.http_session.verify = False
            return self.check_status()
        
        except FastAPIException as error: print(f'{base_message}\nError: {error}')
        except Exception as error: print(f'{base_message}.\nError: {error}')
        
        return False
    
    # NetBox API Endpoint
    app: str = ''
    name: str = ''
    
    # Schemas
    schema = None
    schema_in = None
    schema_list = None
    
    # Unique constraints
    unique_together: list = []
    required_fields: list = []
    
    # Placeholder object
    placeholder_dict: dict = {}
    
    def _generate_hash(self, data):
        try:
            json_string = json.dumps(data, sort_keys=True)  # Convert dictionary to JSON string
            hash_object = hashlib.sha256(json_string.encode('utf-8'))  # Generate SHA-256 hash
            return hash_object.hexdigest()  # Return the hash as a hexadecimal string
        except Exception as error:
            raise FastAPIException(
                message='Error to generate hash object',
                python_exception=str(error)
            )
        
    
    def _hash_object(self, json: dict) -> str:
        return {self._generate_hash(json): json}
    
    def _bootstrap_placeholder(self) -> dict:
        # Parse Pydantic Schema to JSON and construct the JSON object to be used as payload.
        bootstrap: dict = {}
        try:
            json_schema = self.schema_in.model_json_schema()
            for key, value in json_schema['properties'].items():
                default_value = value.get('default', None)
                if default_value:
                    bootstrap[key] = value.get('default')
            
            return bootstrap
        
        except Exception as error:
            raise FastAPIException(
                message=f'Error to create placeholder object {self.app}.{self.name}',
                python_exception=str(error)
            )
    
    def _check_duplicate(
        self,
        json: dict,
        unique_together_json: dict, 
        is_bootstrap: bool,
        cache: bool = True
    ) -> dict:
        try:
            search_dict: dict = {}
            names_to_append = ['type', 'device', 'module_bay', 'device_type', 'role', 'manufacturer', 'cluster_type', 'virtual_machine']
            
            for field in self.unique_together:
                if field in names_to_append:
                    field_id = f'{field}_id'
                    search_dict[field_id] = json.get(field, 0)
                else:
                    search_dict[field] = json.get(field)

            duplicate = self.get(
                **search_dict,
                cache=cache,
                unique_together_json=unique_together_json,
                is_bootstrap=is_bootstrap
            )
            
            if not duplicate:
                return {}
            
            return self.schema(**dict(duplicate)).dict()
            
        except Exception as error:
            return {}

    def _create_object(self,
        json: dict,
        is_bootstrap: bool,
        unique_together_json: dict,
        cache: bool = True
    ) -> dict:
        try:
            result_object: dict = {}
            
            # Create placeholder object if 'bootstrap_placeholder' is True
            try:
                if self.bootstrap_placeholder and self.placeholder_dict:
                    result_object = self.schema(**dict(self.object.create(**self.placeholder_dict))).dict()

                    if cache and is_bootstrap:
                        global_cache.set(
                            key=f'{self.app}.{self.name}.bootstrap',
                            value=result_object
                        )
                    
                    # If object has a schema, it will return the object with the schema
                    return result_object
            except Exception as error:
                raise FastAPIException(
                    message=f'Error to create placeholder object {self.app}.{self.name}',
                    python_exception=str(error)
                )

            try:
                # If 'merge_with_placeholder' is True, it will merge the provided json with the placeholder
                merged_json = self.placeholder_dict | json if self.use_placeholder else json
                print('merged_json: ', merged_json)
                #result_object = self.schema(**dict(self.object.create(**merged_json))).dict()
                result_object = self.schema(**dict(self.object.create(**merged_json)))
                
                if cache and result_object:
                    global_cache.set(
                        key=f'{self.app_name}.{self._generate_hash(unique_together_json)}',
                        value=result_object
                    )
                
                # If object has a schema, it will return the object with the schema
                return result_object
            
            except pynetbox.core.query.RequestError as error:
                msg: str = f'[pynetbox.core.query.RequestError] Error to create object {self.app}.{self.name}'
                raise FastAPIException(
                    message=msg,
                    detail=f'Payload provided: {json}',
                    python_exception=str(error)
                )
            
            except Exception as error:
                raise FastAPIException(
                    message=f'Error to create object {self.app}.{self.name}',
                    python_exception=str(error)
                )
            

        except FastAPIException:
            raise
        
        except Exception as error:
            msg: str = f'[Unexpected Error] Error to create object {self.app}.{self.name}'
            raise FastAPIException(
                message=msg,
                detail=f'Payload provided: {json}',
                python_exception=str(error)
            )
    
    def get(
        self,
        unique_together_json: dict = {},
        id: int = 0,
        cache: bool = False,
        is_bootstrap: bool = False,
        **kwargs
    ) -> dict:
        print('id: ', id)
        try:
            if id:
                get_object = None
                if cache:
                    cache_object = global_cache.get(f'{self.app_name}.{id}') if cache else None
                    if cache_object:
                        return cache_object
                    else:
                        get_object = self.object.get(id)
                

                get_object = self.object.get(id)
                
                if get_object:
                    if cache:
                        global_cache.set(
                            key=f'{self.app_name}.{id}',
                            value=get_object
                        )
                        
                    return self.schema(**dict(get_object)).dict()
                
                return get_object


            if kwargs:
                try:
                    if cache:
                        if is_bootstrap:
                            #print('object is bootstrap')
                            cache_object = global_cache.get(f'{self.app_name}.bootstrap') if cache else None
                            if cache_object:
                                return cache_object
                            
                            get_object = self.schema(**dict(self.object.get(**kwargs))).dict()
                            if get_object:
                                global_cache.set(
                                    key=f'{self.app_name}.bootstrap',
                                    value=get_object
                                )
                            return get_object
                        

                        '''
                        If cache is True, but not a bootstrap object: it will check if the object is in the cache using the hash key.
                        If not, it will get the object from the NetBox API and then cache it for future requests.
                        '''
                        #print('object is not bootstrap, but cached enabled')
                        try:
                            hashed_key = self._generate_hash(data=dict(unique_together_json))
                            #print('hashed_key', hashed_key)
                            cache_object = global_cache.get(f'{self.app_name}.{hashed_key}') if cache else None
                            if cache_object:
                                #print('cache_object found')
                                return cache_object
                            
                            get_object = self.schema(**dict(self.object.get(**kwargs))).dict()
                            if get_object:
                                #print('get_object found, caching it.')
                                global_cache.set(
                                    key=f'{self.app_name}.{hashed_key}',
                                    value=get_object
                                )
                        
                            return get_object
                        except FastAPIException:
                            raise
                        except:
                            raise FastAPIException(
                                message=f'Error to get object {self.app}.{self.name}.',
                                detail='Cache object not found using hash key.',
                                python_exception=str(error)
                            )
                    
                    # If not using cache, it will get the object from the NetBox API
                    # Receives dict, parse to schema and return as dict again.
                    return self.schema(**dict(self.object.get(**kwargs))).dict()

                except ValueError:
                    try:
                        for first_object in self.object.filter(**kwargs):
                            return self.schema(**dict(first_object)).dict()
                        
                    except pynetbox.core.query.RequestError as error:
                        msg: str = f'Error to get object {self.app}.{self.name}\nError: {str(error)}\nPayload provided: {kwargs}'
                        raise FastAPIException(
                            message=msg,
                            python_exception=str(error)
                        )
                
        except requests.exceptions.ConnectionError as error:
            msg: str = f'Connection error to Netbox API ({NETBOX_URL}). Failed to get object {self.app}.{self.name}.'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )

        except Exception as error:
            msg: str = f'Error to get object {self.app}.{self.name}\nPayload provided: {kwargs}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )
            
        
    def post(
        self,
        json: dict,
        merge_with_placeholder: bool = True,
        cache: bool = False,
        is_bootstrap: bool = False,
        **kwargs,
    ):
        unique_together_json = {}
        # Check for missing obrigatory fields
        for field in self.unique_together:
            if json.get(field) is None:
                raise FastAPIException(
                    message=f"Field '{field}' is required to create object {self.app}.{self.name}",
                    status_code=400
                )
            else:
                unique_together_json[field] = json.get(field)
        
        try:
            if is_bootstrap and cache:
                cache_object = global_cache.get(f'{self.app_name}.bootstrap') if cache else None
                if cache_object:
                    return cache_object
                
        except Exception as error:
            raise FastAPIException(
                message=f"Error to check bootstrap object '{self.app}.{self.name}' on cache.",
                python_exception=str(error)
            )
        
        try:
            # Check if object already exists
            duplicate = self._check_duplicate(json, unique_together_json=unique_together_json, cache=cache, is_bootstrap=is_bootstrap)
            if duplicate:
                return duplicate
        except Exception as error:
            raise FastAPIException(
                message=f'Error to check duplicate object {self.app}.{self.name}',
                python_exception=str(error)
            )
        
        try:
            # Create object
            result = self._create_object(
                json=json,
                unique_together_json=unique_together_json,
                cache=cache,
                is_bootstrap=is_bootstrap
            )
            #if self.schema:
            #    return self.schema(**result) if type(result) == dict else result

            print(f'[{self.app}.{self.name}] self.schema not found, returning raw JSON (dict)')
            return result

        except FastAPIException:
            raise
        
        except Exception as error:
            raise FastAPIException(
                message=f'[POST] Error to create object {self.app}.{self.name}.',
                detail="'create_object' method failed",
                python_exception=str(error)
            )
 
    
    def update(self, id: int, json: dict):
        try:
            if self.object.get(id).update(json):
                raise FastAPIException(
                    message=f'Object {self.app}.{self.name} with ID {id} changed successfully.',
                    status_code=200
                )
            else:
                raise FastAPIException(
                    message=f'Object {self.app}.{self.name} with ID {id} not found or change (PUT) failed.',
                    status_code=404
                )
                
        except FastAPIException:
            raise
        
        except pynetbox.core.query.RequestError as error:
            msg: str = f'Error to update object {self.app}.{self.name}'
            raise FastAPIException(
                message=msg,
                detail=f'Payload provided: {json}',
                python_exception=str(error)
            )
        
        except Exception as error:
            msg: str = f'Error to update object {self.app}.{self.name}'
            raise FastAPIException(
                message=msg,
                detail=f'Payload provided: {json}',
                python_exception=str(error)
            )
    
    def delete(self, id: int):
        try:
            search_object = self.object.get(id)
            if search_object:
                if search_object.delete():
                    raise FastAPIException(
                        message=f'Object {self.app}.{self.name} with ID {id} deleted successfully.',
                        status_code=200
                    )

                raise FastAPIException(
                    message=f'Object {self.app}.{self.name} with ID {id} removal failed.',
                    status_code=404
                )
            else:
                raise FastAPIException(
                    message=f'Object {self.app}.{self.name} with ID {id} not found.',
                    status_code=404
                )
                
        except FastAPIException:
            raise

        except pynetbox.core.query.RequestError as error:
            msg: str = f'Error to delete object {self.app}.{self.name}\nError: {str(error)}\nPayload provided: {id}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )

        except Exception as error:
            msg: str = f'Error to delete object {self.app}.{self.name} with ID: {id}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )
    
    def all(self):
        try:
            if self.object.count() == 0:
                return []
            
            if self.schema:
                return [self.schema(**dict(object)).dict() for object in self.object.all()]
            else:
                return self.object.all()
        except Exception as error:
            msg: str = f'Error to get all objects {self.app}.{self.name}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )
    
    class ValueLabelSchema(BaseModel):
        value: str | None = None
        label: Optional[Union[Any, str, int, None]] = None

    class StatusSchema(BaseModel):
        value: str | None = None
        label: str | None = None
    
    class BasicSchema(BaseModel):
        id: int | None = None
        url: str | None = None
        display: str | None = None
        name: str | None = None
        slug: str | None = None
        description: str | None = None