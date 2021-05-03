import json
import requests
import utils
import random
from datetime import datetime
from User import User, load_user

base_server_address = 'http://localhost:'
username = None
password = None
desired_service = None
desired_time = None
tgs_password = None
tgs_ticket = None
service_password = None
expire_at = None
service_ticket = None


def run():
    global username, password
    username = str(input('Username: '))
    password = utils.generate_hash(str(input('Password: ')))
    user = User(username, password)
    user.persist()
    while True:
        print('Actions:')
        print('1 - Authenticate by authentication service')
        print('2 - Request ticket by ticket granting service')
        print('3 - Execute action by resource service')
        desired_action = int(input('Desired action: '))
        execute_action(desired_action)


def execute_action(action):
    if action == 1:
        auth_service()
        return
    if action == 2:
        ticket_granting_service()
        return
    if action == 3:
        resource_service()
        return


def auth_service():
    global desired_service, desired_time, tgs_password, tgs_ticket
    desired_service = int(input('Desired service: '))
    desired_time = int(input('Desired time in minutes: '))
    request_payload = build_m1()
    [response, _] = make_request_to_server('auth_service', '/get_ticket', request_payload)

    payload = json.loads(utils.des_decrypt(response['payload'], password))
    tgs_password = payload['tgs_password']
    tgs_ticket = response['ticket']


def build_m1():
    request = {
        'service_id': desired_service,
        'time': desired_time,
        'proof_number': random.randint(0, 9999),
    }

    return {
        'client_id': username,
        'request': utils.des_encrypt(json.dumps(request), password)
    }


def ticket_granting_service():
    global service_password, expire_at, service_ticket
    request_payload = build_m3()
    [response, _] = make_request_to_server('ticket_granting_service', '/get_ticket', request_payload)

    payload = json.loads(utils.des_decrypt(response['payload'], tgs_password))
    service_password = payload['service_password']
    expire_at = payload['expire_at']
    service_ticket = response['ticket']

    print('Access granted until ' + expire_at + '. Now is ' + format(datetime.now(), '%Y-%m-%d %H:%M:%S'))


def build_m3():
    request = {
        'client_id': username,
        'service_id': desired_service,
        'time': desired_time,
        'proof_number': random.randint(0, 9999),
    }

    return {
        'request': utils.des_encrypt(json.dumps(request), tgs_password),
        'ticket': tgs_ticket,
    }


def resource_service():
    service_id = str(input('Desired service: '))
    desired_resource = str(input('Desired resource: '))
    request_payload = build_m5(desired_resource)
    [response, status_code] = make_request_to_server('service_' + service_id, '/execute_action', request_payload)

    if status_code == 200:
        payload = json.loads(utils.des_decrypt(response['payload'], service_password))
        print(payload['response'])
        return

    if status_code == 400:
        print(response['payload'])


def build_m5(resource):
    request = {
        'client_id': username,
        'expire_at': expire_at,
        'resource': resource,
        'proof_number': random.randint(0, 9999),
    }

    return {
        'request': utils.des_encrypt(json.dumps(request), service_password),
        'ticket': service_ticket,
    }


def make_request_to_server(target, request, request_content):
    url = resolve_target_address(target) + request
    response = requests.post(url, json=request_content)

    return [json.loads(response.text), response.status_code]


def resolve_target_address(target):
    return base_server_address + {
        'auth_service': '7000',
        'ticket_granting_service': '8000',
        'service_1': '9001',
    }[target]


if __name__ == '__main__':
    run()
