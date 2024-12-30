import json
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import os
import dotenv

dotenv.load_dotenv()
client_secret_file = os.getenv('CLIENT_SECRET_FILE')

def authorize_credentials():
    if client_secret_file is None:
        print("Please set the CLIENT_SECRET_FILE environment variable")
        return False
    try:
        CLIENT_SECRET = client_secret_file
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        run_flow(flow, STORAGE, http=http)
        SCOPE = 'https://www.googleapis.com/auth/blogger'
        STORAGE = Storage('credentials.storage.json')
        return True
    except Exception as e:
        return False

def setup_env():
    setup_status = False
    try:
        with open('credentials.storage.json', 'r') as f:
            data = json.load(f)
        env_vars = {}
        with open('.env', 'r') as env_file:
            for line in env_file:
                key, value = line.strip().split('=', 1)
                env_vars[key] = value
        env_vars["CLIENT_ID"] = data["client_id"]
        env_vars["CLIENT_SECRET"] = data["client_secret"]
        env_vars["REFRESH_TOKEN"] = data["refresh_token"]
        with open('.env', 'w') as env_file:
            for key, value in env_vars.items():
                env_file.write(f"{key}={value}\n")
        setup_status = True
        for variable, value in env_vars.items():
            if value == '' or value == 'None':
                if variable == "CLIENT_SECRET_FILE":
                    if env_vars["CLIENT_SECRET"] is not None and env_vars["REFRESH_TOKEN"] is not None and env_vars["CLIENT_ID"] is not None:
                        setup_status = True
                        continue
                    else:
                        setup_status = False
                        break
                print(f"Please set the value for {variable} in the .env file")
                setup_status = False
                break
    except Exception as e:
        print("Error setting up environment variables")
        setup_status = False
    finally:
        return setup_status

def check_authorization():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    refresh_token = os.getenv('REFRESH_TOKEN')
    if client_id is None or client_secret is None or refresh_token is None:
        return False
    else:
        return True

def setup_application():
    if not os.path.exists('.env'):
        print("Create .env file based on example.env")
        return False
    elif check_authorization():
        print("Application authorized successfully")
        return True
    elif not check_authorization() and "credentials.storage.json" in os.listdir():
        print("Please set the environment variables")
        return False
    else:
        authorization_status = authorize_credentials()
        if authorization_status:
            setup_status = setup_env()
            if setup_status:
                print("Application authorized successfully")
                return True
            else:
                print("Please set the environment variables")
                return False
        elif "credentials.storage.json" in os.listdir():
            setup_status = setup_env()
            if setup_status:
                print("Application authorized successfully")
                return True
            else:
                print("Please set the environment variables")
                return False
        else:
            print("Please authorize the application")
            return False    

if __name__ == "__main__":
    setup_application()