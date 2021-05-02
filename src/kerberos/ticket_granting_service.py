import json
import utils
import random
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

tgs_service_password = None


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/get_ticket':
            request = utils.parse_received_request(self)
            response = generate_m4(request)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), 'utf8'))

    def log_message(self, format, *args):
        pass


def generate_m4(request):
    request_ticket = get_request_ticket(request['ticket'])
    client_tgs_password = request_ticket['client_password']
    params = utils.get_request_params(client_tgs_password, request['request'])
    client_service_password = generate_client_service_password()
    expire_at = datetime.now() + timedelta(minutes=int(params['time']))

    payload = {
        'service_password': client_service_password,
        'expire_at': format(expire_at, '%Y-%m-%d %H:%M:%S'),
        'proof_number': params['proof_number'],
    }

    ticket = {
        'client_id': request_ticket['client_id'],
        'expire_at': format(expire_at, '%Y-%m-%d %H:%M:%S'),
        'client_password': client_service_password,
    }

    return {
        'payload': utils.des_encrypt(json.dumps(payload), client_tgs_password),
        'ticket': utils.des_encrypt(json.dumps(ticket), tgs_service_password),
    }


def get_request_ticket(tgs_ticket):
    auth_tgs_password = utils.load_file('auth_tgs', 'our_secret')
    tgs_ticket = utils.des_decrypt(tgs_ticket, auth_tgs_password)
    return json.loads(tgs_ticket)


def generate_client_service_password():
    print('Generating password between client and service')
    password = str(random.randint(0, 9999))
    return utils.generate_hash(password)


def generate_tgs_service_password():
    global tgs_service_password
    print('Generating password between tgs and services')
    password = str(random.randint(0, 9999))
    tgs_service_password = utils.generate_hash(password)
    utils.persist_txt('tgs_service', 'our_secret', tgs_service_password)


def run(server_class=HTTPServer, handler_class=Handler):
    generate_tgs_service_password()
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print('Ticket granting service initialized')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
