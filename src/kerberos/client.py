import json
import requests
import utils
import random
from User import User, load_user

base_server_address = 'http://localhost:'
username = None
password = None
tgs_password = None
tgs_ticket = None


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
    global tgs_password, tgs_ticket
    desired_service = int(input('Desired resource: '))
    desired_time = int(input('Desired time in minutes: '))
    request_payload = build_m1(desired_service, desired_time)
    response = make_request_to_server('auth_service', '/get_ticket', request_payload)

    payload = json.loads(utils.des_decrypt(response['payload'], password))
    tgs_password = payload['tgs_password']
    tgs_ticket = response['ticket']


def build_m1(desired_service, desired_time):
    request = {
        'service_id': desired_service,
        'time': desired_time,
        'proof_number': random.randint(0, 9999),
    }

    return {
        'client_id': username,
        'request': utils.des_encrypt(json.dumps(request), password)
    }


def make_request_to_server(target, request, request_content):
    url = resolve_target_address(target) + request
    response = requests.post(url, json=request_content)

    return json.loads(response.text)


def resolve_target_address(target):
    return base_server_address + {
        'auth_service': '7000'
    }[target]


if __name__ == '__main__':
    run()
