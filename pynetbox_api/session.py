import requests
import urllib3
import pynetbox
from pynetbox_api.exceptions import FastAPIException

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

NETBOX_URL = os.getenv('NETBOX_URL')
NETBOX_TOKEN = os.getenv('NETBOX_TOKEN')

print(NETBOX_URL, NETBOX_TOKEN)
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
    def __new__(cls, **kwargs):
        # Create a new instance of the class
        instance = super().__new__(cls)
        
        # Check if the instance is being created with arguments
        if kwargs: 
            # Initialize attributes
            instance.app = ''
            instance.name = ''
            instance.schema = None
            unique_together: list = []
            instance.object = getattr(getattr(nb, cls.app), cls.name)
            
            # Return post method result as the class instance
            return instance.post(kwargs)
        else:
            # Return the instance as is if not being created with arguments
            return instance
        
    def __init__(self, **kwargs):
        # Only initialize if the instance is being created (not when post method is used)
        if not kwargs:
            try:
                self.object = getattr(getattr(nb, self.app), self.name)
            except Exception as error:
                print(f'Error to get object {self.app}.{self.name}\nError: {str(error)}')

    
    app: str = ''
    name: str = ''
    schema: None
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

                else:
                    search_dict[field] = json.get(field)
                
                duplicate = self.get(multiple_values=search_dict)
            else:
                duplicate = self.get(value=json.get(self.unique_together[0]))
            
            if not duplicate:
                return None
            
            if self.schema:
                return self.schema(**dict(duplicate))
            else:
                return dict(duplicate)
            
        except Exception as error:
            print(error)
            return None
    
    def get(
        self,
        value: str = '',
        multiple_values: dict = [],
        id: int = 0
    ):
        try:
            if id:
                return self.object.get(id)
            if multiple_values:
                try:
                    return self.object.get(**multiple_values)
                except ValueError:
                    print('Error to get object, multiple objects found. Returning the first one.')
                    print(multiple_values, self.app, self.name)
                    try:
                        for first_object in self.object.filter(**multiple_values):
                            return first_object
                        
                    except pynetbox.core.query.RequestError as error:
                        msg: str = f'Error to get object {self.app}.{self.name}\nError: {str(error)}\nPayload provided: {multiple_values}'
                        raise FastAPIException(
                            message=msg,
                            python_exception=str(error)
                        )
                        
            if self.name == ('interfaces' or 'module_bays'):
                if not id:
                        return self.object.filter(name=value)
            if self.unique_together == 'name':
                return self.object.get(name=value)
            if self.unique_together == 'model':
                return self.object.get(model=value)
            if self.unique_together == 'address':
                return self.object.get(address=value) 
            if self.unique_together == 'ssid':
                return self.object.get(ssid=value) 
                
        except requests.exceptions.ConnectionError as error:
            msg: str = f'Connection error to Netbox API ({NETBOX_URL}). Failed to get object {self.app}.{self.name}.'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )

        except Exception as error:
            msg: str = f'Error to get object {self.app}.{self.name}\nError: {str(error)}\nPayload provided: {multiple_values}'
            raise FastAPIException(
                message=msg,
                python_exception=str(error)
            )
            
        
    
    def post(self, json: dict):
        def create_object(object, json):
            try:
                result_object = dict(object.create(**json))
                if self.schema:
                    return self.schema(**result_object)
                else:
                    return result_object

            except pynetbox.core.query.RequestError as error:
                msg: str = f'Error to create object {self.app}.{self.name}\nError: {str(error)}\nPayload provided: {json}'
                raise FastAPIException(
                    message=msg,
                    python_exception=str(error)
                )
        
        # If the object is a interface or module_bay, it will check if the interface or module_bay already exists
        # by using the device id, if it exists, it will return the object, if not, it will create the object
        duplicate = self._check_duplicate(json)
        if duplicate is None:
            result = create_object(object=self.object, json=json)
            return result
        else:
            return duplicate