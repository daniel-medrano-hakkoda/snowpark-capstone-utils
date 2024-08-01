import os
from getpass import getpass
import configparser
from snowflake.snowpark import Session

DEFAULT_CONFIG_FILE_PATH = './snowflake_creds.config'
DEFAULT_ACCOUNT = 'jsa18243'
DEFAULT_USER =  'your_name@hakkoda.io'
DEFAULT_ROLE = 'DATA_ENGINEER'
DEFAULT_WAREHOUSE = 'COMPUTE_WH'
DEFAULT_DATABASE = 'SNOWPARK_CAPSTONE_DB'
DEFAULT_SCHEMA = 'MY_SCHEMA'

# Function to load credentials from a config file
def _load_credentials_from_file(file_path: str) -> dict[str, str]:
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['default']

# Function to get input from the user with a default value option
def _get_input(prompt: str, default: str = '') -> str:
    user_input = input(f"{prompt} (default: {default}): ").strip()
    return user_input if user_input else default

# Function to get credentials from the user
def _get_credentials_from_user() -> dict[str, str]:
    account = _get_input('Enter your Snowflake account identifier', DEFAULT_ACCOUNT)
    user = _get_input('Enter your Snowflake username', DEFAULT_USER)
    role = _get_input('Enter your Snowflake role', DEFAULT_ROLE)
    warehouse = _get_input('Enter your Snowflake warehouse', DEFAULT_WAREHOUSE)
    database = _get_input('Enter your Snowflake database', DEFAULT_DATABASE)
    schema = _get_input('Enter your Snowflake schema', DEFAULT_SCHEMA)

    credentials = {
        'account': account,
        'user': user,
        'role': role,
        'warehouse': warehouse,
        'database': database,
        'schema': schema
    }

    # Ask the user to choose between password or SSO authentication
    auth_type = _get_input('Choose authentication method (password/sso)', 'password').strip().lower()
    if auth_type == 'password':
        credentials['password'] = getpass('Enter your Snowflake password: ')
    elif auth_type == 'sso':
        credentials['authenticator'] = 'externalbrowser' # SSO via external browser
    else:
        raise Exception('Invalid authentication method. Please restart and choose either "password" or "sso".')

    return credentials

# Function to save credentials to a config file
def _save_credentials_to_file(credentials: dict[str, str], file_path: str) -> None:
    config = configparser.ConfigParser()
    config['default'] = credentials
    with open(file_path, 'w') as configfile:
        config.write(configfile)

def _process_credentials_from_user(config_file_path: str) -> dict[str, str]:
    # Get and ask if the user wants to save the credentials in a file
    credentials = _get_credentials_from_user()
    save_to_file = _get_input('Do you want to save these credentials to a config file for future use? (yes/no)', 'yes').strip().lower()
    if save_to_file == 'yes':
        _save_credentials_to_file(credentials, config_file_path)
    return credentials

# Function to create a Snowflake session
def create_session() -> Session:
    # Get the config file path
    config_file_path = _get_input('Enter the path to your config file', DEFAULT_CONFIG_FILE_PATH)
    
    # Check if the config file exists
    if os.path.exists(config_file_path):
        use_existing_file = _get_input('Config file found. Do you want to use it? (yes/no)', 'yes').strip().lower()
        if use_existing_file == 'yes':
            credentials = _load_credentials_from_file(config_file_path)
        else:
            credentials = _process_credentials_from_user(config_file_path)
    else:
        credentials = _process_credentials_from_user(config_file_path)

    if credentials:
        # Store credentials in environment variables
        os.environ.update(credentials)
        # Create and return the Snowflake session
        return Session.builder.configs(credentials).create()