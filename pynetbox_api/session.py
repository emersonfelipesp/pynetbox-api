import requests
import urllib3
import pynetbox
from typing import (
    Any,
    Annotated,
    Dict,
    List,
)

from typing_extensions import Doc

from fastapi.responses import JSONResponse
from pynetbox_api.exceptions import FastAPIException

urllib3.disable_warnings()

session = requests.Session()
session.verify = False

NETBOX_URL = None
NETBOX_TOKEN = NOEN

try:
    from env import NETBOX_URL, NETBOX_TOKEN
    
    if not NETBOX_URL:
        raise FastAPIException(
            message='NETBOX_URL environment variable not found.',
            status_code=500
        )
    if not NETBOX_TOKEN:
        raise FastAPIException(
            message='NETBOX_TOKEN environment variable not found.',
            status_code=500
        )
except FastAPIException:
    raise

except ImportError as error:
    raise FastAPIException(
        message='Error to load environment variables.',
        python_exception=str(error)
    )
    
try:
    if NETBOX_URL and NETBOX_TOKEN:
        nb = pynetbox.api(
            NETBOX_URL,
            token=NETBOX_TOKEN,
        )

except Exception as error:
    raise FastAPIException(
        message=f'Error to connect to Netbox ({NETBOX_URL})',
        python_exception=str(error)
    )

nb.http_session = session

class NetBoxBase:
    """
    Helper class to interact with NetBox API using pynetbox library.
    
    Attributes:
        use_placeholder: Define is placeholder object will be used to create new objects, filling missing fields.
        bootstrap_placeholder: Define if placeholder object will be created during class instantiation or if no object is provided.
    """
    def __new__(cls, use_placeholder: bool = True, bootstrap_placeholder: bool = False, **kwargs):
        # Create a new instance of the class
        instance = super().__new__(cls)
        
        # Check if the instance is being created with arguments
        if kwargs:
            try:
                instance.use_placeholder = use_placeholder
                instance.bootstrap_placeholder = bootstrap_placeholder
                
                instance.object = getattr(getattr(nb, instance.app), instance.name)
                
                if instance.use_placeholder or instance.bootstrap_placeholder:
                    instance.placeholder_dict = instance._bootstrap_placeholder()
            
                print('instance.object', instance.object)
            except Exception as error:
                raise FastAPIException(
                    message=f'Error to get object {instance.app}.{instance.name}',
                    detail='__new__ method',
                    python_exception=str(error)
                )
            
            # Return post method result as the class instance
            result = instance.post(kwargs, merge_with_placeholder=use_placeholder)
            return result if result else {}

        else:
            # Return the instance as is if not being created with arguments
            return instance
        
    def __init__(
        self,
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
        **kwargs):
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
            self.result = self.post(self.placeholder_dict)

    
    app: str = ''
    name: str = ''
    schema = None
    schema_in = None
    schema_list = None
    unique_together: list = []
    placeholder_dict: dict = {}
    
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
    
    def _check_duplicate(self, json: dict):
        try:

            search_dict: dict = {}
            for field in self.unique_together:
                if field == 'device':
                    device_id = int(json.get(field, 0))
                    if device_id > 0:
                        search_dict['device_id'] = device_id
                        
                elif field == 'module_bay':
                    module_bay_id = int(json.get(field, 0))
                    if module_bay_id > 0:
                        search_dict['module_bay_id'] = module_bay_id
                        
                elif field == 'device_type':
                    device_type_id = int(json.get(field, 0))
                    if device_type_id > 0:
                        search_dict['device_type_id'] = device_type_id
                
                elif field == 'role':
                    role_id = int(json.get(field, 0))
                    if role_id > 0:
                        search_dict['role_id'] = role_id
                        
                elif field == 'manufacturer':
                    manufacturer_id = int(json.get(field, 0))
                    if manufacturer_id > 0:
                        search_dict['manufacturer_id'] = manufacturer_id

                else:
                    search_dict[field] = json.get(field)
                
            duplicate = self.get(**search_dict)
            
            if not duplicate:
                return None
            
            if self.schema:
                return self.schema(**dict(duplicate)).model_dump()
            else:
                return dict(duplicate)
            
        except Exception as error:
            return None

    def _create_object(self, json: dict):
        try:
            result_object: dict = {}
            
            # Create placeholder object if 'bootstrap_placeholder' is True
            try:
                if self.bootstrap_placeholder and self.placeholder_dict:
                    result_object = dict(self.object.create(**self.placeholder_dict))
                    
                    # If object has a schema, it will return the object with the schema
                    return self.schema(**result_object) if self.schema else result_object
            except Exception as error:
                raise FastAPIException(
                    message=f'Error to create placeholder object {self.app}.{self.name}',
                    python_exception=str(error)
                )

            try:
                # If 'merge_with_placeholder' is True, it will merge the provided json with the placeholder
                merged_json = self.placeholder_dict | json if self.use_placeholder else json
                result_object = dict(self.object.create(**merged_json))
                
                # If object has a schema, it will return the object with the schema
                return self.schema(**result_object) if self.schema else result_object
            
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
        id: int = 0,
        **kwargs
    ):
        try:
            if id:
                return self.object.get(id)
            if kwargs:
                try:
                    return self.object.get(**kwargs)
                except ValueError:
                    try:
                        for first_object in self.object.filter(**kwargs):
                            return first_object
                        
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
            
        
    def post(self, json: dict, merge_with_placeholder: bool = True):
        # Check for missing obrigatory fields
        for field in self.unique_together:
            if json.get(field) is None:
                raise FastAPIException(
                    message=f"Field '{field}'' is required to create object {self.app}.{self.name}",
                    status_code=400
                )
        
        try:
            # Check if object already exists
            duplicate = self._check_duplicate(json)
            if duplicate:
                return duplicate
        except Exception as error:
            raise FastAPIException(
                message=f'Error to check duplicate object {self.app}.{self.name}',
                python_exception=str(error)
            )
        
        try:
            # Create object
            result = self._create_object(json=json)
            if result:
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
                return [self.schema(**dict(object)) for object in self.object.all()]
            else:
                return self.object.all()
        except Exception as error:
            msg: str = f'Error to get all objects {self.app}.{self.name}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )