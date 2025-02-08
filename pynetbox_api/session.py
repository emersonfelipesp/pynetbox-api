import requests
import urllib3
import pynetbox

from fastapi.responses import JSONResponse
from pynetbox_api.exceptions import FastAPIException

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

NETBOX_URL = os.getenv('NETBOX_URL')
NETBOX_TOKEN = os.getenv('NETBOX_TOKEN')

urllib3.disable_warnings()

session = requests.Session()
session.verify = False

try:
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

'''
unique_together: dict = {
    'dcim': {
        'sites': 'name',
        'manufacturers': 'name',
        'device_roles': 'name',
        'device_types': 'model',
        'cables': 'id',
        'devices': ['name', 'device_type', 'role'],
        'interfaces': ['device', 'name'],
        'module_bays': ['device', 'name'],
        'module_types': 'model',
        'modules': ['device', 'module_bay'],
        'rear_ports': ['device', 'name'],
        'front_ports': ['device', 'name', 'rear_port']
    },
    'ipam': {
        'ip_addresses': 'address'
    },
    'extras': {
        'custom_fields': 'name'
    },
    'wireless': {
        'wireless_lans': 'ssid'
    }
}
'''


class NetBoxBase:
    def __new__(cls, use_placeholder: bool | None = None, **kwargs):
        # Create a new instance of the class
        instance = super().__new__(cls)
        
        # Check if the instance is being created with arguments
        if kwargs and not use_placeholder: 
            # Initialize attributes
            instance.app = ''
            instance.name = ''
            instance.schema = None
            instance.schema_in = None
            instance.schema_list = None
            instance.unique_together = []
            instance.object = getattr(getattr(nb, cls.app), cls.name)
            
            # Return post method result as the class instance
            return instance.post(kwargs)
        else:
            # Return the instance as is if not being created with arguments
            return instance
        
    def __init__(self, use_placeholder: bool | None = None, **kwargs):
        # Only initialize if the instance is being created (not when post method is used)
        if not kwargs:
            try:
                self.object = getattr(getattr(nb, self.app), self.name)
            except Exception as error:
                print(f'Error to get object {self.app}.{self.name}\nError: {str(error)}')
                
        self.use_placeholder = use_placeholder
        if self.use_placeholder:
            # Parse Pydantic Schema to JSON and construct the JSON object to be used as payload.
            try:
                self.placeholder_dict: dict = {}
                json_schema = self.schema_in.model_json_schema()
                for key, value in json_schema['properties'].items():
                    default_value = value.get('default', None)
                    if default_value:
                        self.placeholder_dict[key] = value.get('default')
                
            except Exception as error:
                raise FastAPIException(
                    message=f'Error to create placeholder object {self.app}.{self.name}',
                    python_exception=str(error)
                )

        if self.use_placeholder and self.placeholder_dict:
            self.object = self.post(self.placeholder_dict)

    
    app: str = ''
    name: str = ''
    schema = None
    schema_in = None
    schema_list = None
    unique_together: list = []
    
    
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
            
    
    def post(self, json: dict):
        def create_object(object, json):
            try:
                # Create placeholder object if 'use_placeholder' is True
                if self.use_placeholder and self.placeholder_dict:
                    result_object = dict(object.create(**self.placeholder_dict))
                    
                # Create object with provided json
                else:
                    result_object = dict(object.create(**json))
                
                # If object has a schema, it will return the object with the schema
                if self.schema:
                    return self.schema(**result_object)
                
                # If not, it will return the object as a dict
                else:
                    return result_object

            except pynetbox.core.query.RequestError as error:
                msg: str = f'Error to create object {self.app}.{self.name}'
                raise FastAPIException(
                    message=msg,
                    detail=f'Payload provided: {json}',
                    python_exception=str(error)
                )
            
            except Exception as error:
                msg: str = f'Error to create object {self.app}.{self.name}'
                raise FastAPIException(
                    message=msg,
                    detail=f'Payload provided: {json}',
                    python_exception=str(error)
                )
        
        # If the object is a interface or module_bay, it will check if the interface or module_bay already exists
        # by using the device id, if it exists, it will return the object, if not, it will create the object
        try:
            duplicate = self._check_duplicate(json)
            if duplicate:
                return duplicate
            
            result = create_object(object=self.object, json=json)
            if result:
                print(result)
                return result

        except Exception as error:
            raise FastAPIException(
                message=f'Error to create object {self.app}.{self.name}.',
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