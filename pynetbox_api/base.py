import json
import hashlib
from typing import Optional, Union, Any
from typing_extensions import Annotated, Doc
from abc import abstractmethod
import pynetbox
import requests
from pydantic import BaseModel


# Import custom exceptions and cache
from pynetbox_api.exceptions import FastAPIException
from pynetbox_api.cache import global_cache
from pynetbox_api.logger import logger

# Global variables that need to be defined
NETBOX_STATUS = False
NETBOX_SESSION = None
NETBOX_URL = None  # This should be set elsewhere in your application

class NetBoxBase:
    """
    Helper class to interact with NetBox API using pynetbox library.
    
    Attributes:
        use_placeholder: Define is placeholder object will be used to create new objects, filling missing fields.
        bootstrap_placeholder: Define if placeholder object will be created during class instantiation or if no object is provided.
    """
    
    
    def __init__(
        self,
        nb: pynetbox.api | None = None,
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
                Define if placeholder object will be used to create new objects, filling missing fields.
                It will use the pydantic schema to create the placeholder object.
                The schema is defined in the class as 'schema_in'.
                """
            )
        ] = False,
        **kwargs
    ):

        if nb:
            self.nb = nb
        else:
            self.nb = self.__class__.nb
        
        if not self.nb:
            raise FastAPIException(
                message='No NetBox API connection provided.',
                detail='__init__ method'
            )
        
        self.id = 0
        self.app_name = f'{self.app}.{self.name}'
        self.kwargs = kwargs
        
        if not self.check_status(): return
        
        try:
            if self.nb:
                self.object = getattr(getattr(self.nb, self.app), self.name)
            else:
                return None
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
            self.json = self.result
            self.id = None
            try:
                self.id = self.result.get('id', None)
            except:
                self.id = getattr(self.result, 'id', None)
                
        # Check if the instance is being created with arguments
        if kwargs and not bootstrap_placeholder:
            # Return post method result as the class instance
            result: dict = self.post(
                json=kwargs,
                cache=True,
                merge_with_placeholder=True
            )

            self.id = result.get('id', None) if type(result) == dict else None
            self.id = getattr(result, 'id', None) if type(result) != dict else None
            
            self.result = result if type(result) == dict else result.model_dump()
            self.json = self.result  # Set json property to match result
            self.id = self.result.get('id', None) if type(self.result) == dict else None

    # Shared placeholder object between all instances of the class (subclass-aware)
    _placeholder = None
    
    @property
    def placeholder(self):
        if self.__class__._placeholder is None:
            # Get default values from the schema
            default_values = self.schema_in().model_dump(exclude_none=True)
            
            try:
                # Check if the object already exists on NetBox
                check_duplicate = self.object.get(**default_values)
            except ValueError as error:
                raise FastAPIException(
                    message=f'Error to get object {self.app}.{self.name}',
                    python_exception=str(error)
                )
    
            
            # If the object already exists, return the object
            if check_duplicate:
                self.__class__._placeholder = check_duplicate
            else:
                # Base on the default values, create a placeholder object on NetBox
                self.__class__._placeholder = self.schema(**dict(self.object.create(default_values))).model_dump()

        # Return the placeholder object
        return self.__class__._placeholder
    
    def __dict__(self) -> dict:
        """
        Return the result attribute when dict() is called on the instance.
        This allows dict(NetBoxBase()) to return the result attribute.
        """
        return getattr(self, 'result', {})


    def __iter__(self):
        """
        Make the object iterable so dict() can work properly.
        This iterates over the result attribute if it's a dictionary.
        """
        result = getattr(self, 'result', {})
        if isinstance(result, dict):
            return iter(result.items())
        return iter({}.items())


    def __getitem__(self, key):
        """
        Allow dictionary-style access to the result attribute.
        """
        result = getattr(self, 'result', {})
        if isinstance(result, dict):
            return result[key]
        raise KeyError(key)


    def dict(self) -> dict:
        """
        Explicit method to get the result as a dictionary.
        """
        return getattr(self, 'result', {})

    def __call__(self, bootstrap_placeholder: bool = False, **kwargs):
        """
        Make NetBoxBase instances callable to create new objects.
        This allows usage like: nb_api.dcim.manufacturer(name='test', slug='test')
        """
        result = self.post(json=kwargs, cache=True)
        # Update the instance with the result
        if isinstance(result, dict):
            self.result = result
            self.json = result
            self.id = result.get('id', None)
        return self


    def check_status(self) -> bool:
        global NETBOX_STATUS, NETBOX_SESSION
        base_message: str = 'Unexpected error to connect to NetBox API using check_status() method.'
        try:
            if NETBOX_STATUS == False or NETBOX_SESSION is None:
                logger.info('Trying to get NetBox API status...')
                self.nb.status()
                logger.info('NetBox API status received successfully.')
                NETBOX_STATUS = True
                NETBOX_SESSION = self.nb
                return NETBOX_STATUS
            else:
                return NETBOX_STATUS
        except pynetbox.core.query.ContentError as error:
            logger.error(f'Error to connect to NetBox API. The API URL is invalid.\n{error}')
            NETBOX_STATUS = False
            NETBOX_SESSION = None
        except pynetbox.RequestError as error:
            logger.error(f'Error to connect to NetBox API.\nError: {error}')
            NETBOX_STATUS = False
            NETBOX_SESSION = None
        except requests.exceptions.SSLError as error:
            # Error: HTTPSConnectionPool(host='10.0.30.200', port=443): Max retries exceeded with url: /api/status/
            # (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1000)')))
            # This error happens when the certificate is self-signed.
            # The "solution" is to disable the SSL verification.
            logger.error(f'SSL Error trying to connect to NetBox API.\nError: {error}')
            self.nb.http_session.verify = False
            return self.check_status()
        
        except FastAPIException as error: 
            logger.error(f'{base_message}\nError: {error}')
            NETBOX_STATUS = False
            NETBOX_SESSION = None
        except Exception as error: 
            logger.error(f'{base_message}.\nError: {error}')
            NETBOX_STATUS = False
            NETBOX_SESSION = None
        
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
    json: dict = {}
    result: dict = {}

    
    nb: pynetbox.api | None = None
    
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
        # Get all values from the schema instance, excluding unset values
        try:
            bootstrap_default_values = self.schema_in().model_dump(exclude_none=True)
            return bootstrap_default_values
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
        '''
        This code is part of a method `_check_duplicate` that checks for duplicate objects based on unique constraints.
        It constructs a `search_dict` using fields defined in `self.unique_together`.
        If a field is in the `names_to_append` list, it appends '_id' to the field name and retrieves its value from the `json` dictionary.
        Otherwise, it directly retrieves the field's value from the `json` dictionary.
        The method then attempts to find a duplicate object using the constructed `search_dict`.
        If a duplicate is found, it returns the object as a dictionary using the schema; otherwise, it returns an empty dictionary.
        '''
            
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
            
            return self.schema(**dict(duplicate)).model_dump()
            
        except Exception as error:
            return {}

    def _create_object(self,
        json: dict,
        is_bootstrap: bool,
        unique_together_json: dict,
        cache: bool = True,
        use_placeholder: bool = True
    ) -> dict:
        try:
            result_object: dict = {}
            
            # Create placeholder object if 'bootstrap_placeholder' is True
            try:
                if self.bootstrap_placeholder and self.placeholder_dict:
                    result_object = self.schema(**dict(self.object.create(**self.placeholder_dict))).model_dump()

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
        try:
            if id:
                get_object = None
                if cache:
                    cache_object = global_cache.get(f'{self.app_name}.{id}') if cache else None
                    if cache_object:
                        return cache_object


                get_object = self.object.get(id)
                
                if get_object:
                    if cache:
                        global_cache.set(
                            key=f'{self.app_name}.{id}',
                            value=get_object
                        )
                
                json_object = self.schema(**dict(get_object)).model_dump() if self.schema else get_object
                self.result = json_object
                self.id = json_object.get('id', None)
                self.json = json_object
                
                return json_object



            if kwargs:
                try:
                    if cache:
                        if is_bootstrap:
                            cache_object = global_cache.get(f'{self.app_name}.bootstrap') if cache else None
                            if cache_object:
                                return cache_object
                            
                            get_object = self.schema(**dict(self.object.get(**kwargs))).model_dump()
                            if get_object:
                                global_cache.set(
                                    key=f'{self.app_name}.bootstrap',
                                    value=get_object
                                )
                                
                            self.result = get_object
                            self.id = get_object.get('id', None)
                            self.json = get_object
                            
                            return get_object
                        

                        '''
                        If cache is True, but not a bootstrap object: it will check if the object is in the cache using the hash key.
                        If not, it will get the object from the NetBox API and then cache it for future requests.
                        '''
                        try:
                            hashed_key = self._generate_hash(data=dict(unique_together_json))
                            cache_object = global_cache.get(f'{self.app_name}.{hashed_key}') if cache else None
                            if cache_object:
                                self.result = cache_object
                                self.id = cache_object.get('id', None)
                                self.json = cache_object
                                return cache_object
                            
                            get_object = self.schema(**dict(self.object.get(**kwargs))).model_dump()
                            if get_object:
                                global_cache.set(
                                    key=f'{self.app_name}.{hashed_key}',
                                    value=get_object
                                )
                            
                            self.result = get_object
                            self.id = get_object.get('id', None)
                            self.json = get_object
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
                    get_object = self.schema(**dict(self.object.get(**kwargs))).model_dump()
                    self.result = get_object
                    self.id = get_object.get('id', None)
                    self.json = get_object
                    return get_object

                except ValueError:
                    try:
                        for first_object in self.object.filter(**kwargs):
                            get_object = self.schema(**dict(first_object)).model_dump()
                            self.result = get_object
                            self.id = get_object.get('id', None)
                            self.json = get_object
                            return get_object
                        
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
        '''
        Create a new object in NetBox.
        '''
        
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
            raise FastAPIException(message=f"Error to check bootstrap object '{self.app}.{self.name}' on cache.", python_exception=str(error))
        
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

            logger.info(f'[{self.app}.{self.name}] self.schema not found, returning raw JSON (dict)')
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
        '''
        Update an object in NetBox.
        '''
        
        try:
            if self.object.get(id).update(json):
                raise FastAPIException(message=f'Object {self.app}.{self.name} with ID {id} changed successfully.', status_code=200)
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
    
    def delete(self):
        try:
            search_object = self.object.get(self.id)
            if search_object:
                if search_object.delete():
                    self.id = None
                    self.result = {}
                    return True
                    
                    '''
                    raise FastAPIException(
                        message=f'Object {self.app}.{self.name} with ID {self.id} deleted successfully.',
                        status_code=200
                    )
                    '''

                return False
                '''
                raise FastAPIException(
                    message=f'Object {self.app}.{self.name} with ID {self.id} removal failed.',
                    status_code=404
                )
                '''
            else:
                return False
                '''
                raise FastAPIException(
                    message=f'Object {self.app}.{self.name} with ID {self.id} not found.',
                    status_code=404
                )
                '''
                
        except FastAPIException:
            return False
            # raise

        except pynetbox.core.query.RequestError as error:
            return False
            '''
            msg: str = f'Error to delete object {self.app}.{self.name}\nError: {str(error)}\nPayload provided: {id}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )
            '''

        except Exception as error:
            return False
            
            '''
            msg: str = f'Error to delete object {self.app}.{self.name} with ID: {id}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )
            '''
    
    def all(self):
        try:
            if self.object.count() == 0:
                return []
            
            if self.schema:
                return [self.schema(**dict(object)).model_dump() for object in self.object.all()]
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