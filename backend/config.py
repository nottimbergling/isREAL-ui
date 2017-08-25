import sys
import socket
from pprint import pformat


# Global config
logger_name = "peachme"


# Default values, also helps code completion
name = None
logger_path = None
frontend_path = "../frontend/"


mongo_server = "localhost"
database = "isreal"
port = 27017
# user = "isreal"
# password = "isreal"

# Environment configs
prod_config = {
    "name": "Prod configuration"
}


test_config = {
    "name": "Test configuration",
    "logger_path": """C:\code\logs\peachme.log"""
}


_config_mapping = {
    "default": prod_config,
    "david-pc": test_config,
    "desktop-5pp675l": test_config
}


# Logic of choosing config based on hostname
_hostname = socket.gethostname().lower()
_relevant_configuration = _config_mapping[_hostname] if _hostname in _config_mapping else _config_mapping["default"]


# Set module attributes
for key in _relevant_configuration:
    sys.modules[__name__].__setattr__(key, _relevant_configuration[key])


# Function will run at str(config)
def to_string(self):
    return pformat(self)
sys.modules[__name__].__str__ = to_string
