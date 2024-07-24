import os
from getpass import getpass
import configparser
from snowflake.snowpark import Session

__version__ = '0.1.0'

# Define the path to the credentials file in Google Drive
config_file_path = './snowflake_creds.config'

# Function to load credentials from a config file
def _load_credentials_from_file(file_path: str) -> dict[str, str]:
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['default']

# Function to get credentials from the user
def _get_credentials_from_user() -> dict[str, str]:
    credentials = {
        'account': input('Enter your Snowflake account identifier: '),
        'user': getpass('Enter your Snowflake username: '),
        'role': input('Enter your Snowflake role: '),
        'warehouse': input('Enter your Snowflake warehouse: '),
        'database': input('Enter your Snowflake database: '),
        'schema': input('Enter your Snowflake schema: ')
    }

    # Ask the user to choose between password or SSO authentication
    auth_type = input('Choose authentication method (password/sso): ').strip().lower()
    if auth_type == 'password':
        credentials['password'] = getpass('Enter your Snowflake password: ')
        return credentials
    if auth_type == 'sso':
        credentials['authenticator'] = 'externalbrowser'  # SSO via external browser
        return credentials
    raise Exception('Invalid authentication method. Please restart and choose either "password" or "sso".')

# Function to save credentials to a config file
def _save_credentials_to_file(credentials: dict[str, str], file_path: str) -> None:
    config = configparser.ConfigParser()
    config['default'] = credentials
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# Function to create a Snowflake session
def create_session() -> Session:
  # Check if the config file exists
  if os.path.exists(config_file_path):
      use_existing_file = input('Config file found. Do you want to use it? (yes/no): ').strip().lower()
      if use_existing_file == 'yes':
          credentials = _load_credentials_from_file(config_file_path)
      else:
          credentials = _get_credentials_from_user()
  else:
      credentials = _get_credentials_from_user()

  if credentials:
      # Store credentials in environment variables
      os.environ.update(credentials)

      # Ask if the user wants to save the credentials in a file
      save_to_file = input('Do you want to save these credentials to a config file for future use? (yes/no): ').strip().lower()
      if save_to_file == 'yes':
          _save_credentials_to_file(credentials, config_file_path)

      return Session.builder.configs(credentials).create()