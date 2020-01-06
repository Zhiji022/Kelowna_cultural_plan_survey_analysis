# data loader for getting login credentials for the dashboard
import json
from cryptography.fernet import Fernet

fernet_key_file = open('./fernet_key.key', 'rb')
fernet_key = fernet_key_file.read() # The key will be type bytes
fernet_key_file.close()

user_login_keys_file = open('./username_password.key', 'rb')
user_login_keys = user_login_keys_file.read()
user_login_keys_file.close()

fernet = Fernet(fernet_key)
user_login_keys = json.loads(fernet.decrypt(user_login_keys).decode())

def get_user_login_keys():
    return user_login_keys
