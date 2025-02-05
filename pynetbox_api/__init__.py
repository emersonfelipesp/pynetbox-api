from dotenv import load_dotenv
import os

from .netbox import nb

# Load environment variables from .env file
load_dotenv()

NETBOX_URL = os.getenv('NETBOX_URL')
NETBOX_TOKEN = os.getenv('NETBOX_TOKEN')