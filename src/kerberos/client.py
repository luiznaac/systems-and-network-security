import json
import requests
import utils
from User import User, load_user

base_server_address = 'http://localhost:'
username = None
password = None


def run():
    global username, password
    username = str(input('Username: '))
    password = utils.generate_hash(str(input('Password: ')))
    user = User(username, password)
    user.persist()
    while True:
        print('Actions:')
        print('1 - Authenticate by authentication service')
        desired_action = int(input('Desired action: '))
        execute_action(desired_action)


def execute_action(action):
    if action == 1:
        auth_service()


def auth_service():
    desired_service = 1
    desired_time = int(input('Desired time in minutes: '))
    encrypted_data = utils.des_encrypt('testing', password)


def make_request_to_server(target, request, request_content):
    url = resolve_target_address(target) + request
    response = requests.post(url, json=request_content)

    return json.loads(response.text)


def resolve_target_address(target):
    return base_server_address + {

    }[target]


if __name__ == '__main__':
    run()
