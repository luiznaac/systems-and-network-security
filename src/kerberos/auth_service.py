import json
import utils
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

auth_tgs_password = None


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/get_ticket':
            request = utils.parse_received_request(self)
            print(request['client_id'] + ' requested a tgs ticket')
            response = generate_m2(request)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), 'utf8'))

    def log_message(self, format, *args):
        pass


def generate_m2(request):
    client_id = request['client_id']
    client_password = utils.load_file('users', client_id)
    params = utils.get_request_params(client_password, request['request'])

    client_tgs_password = generate_client_tgs_password()

    payload = {
        'tgs_password': client_tgs_password,
        'proof_number': params['proof_number'],
    }

    ticket = {
        'client_id': client_id,
        'time': params['time'],
        'client_password': client_tgs_password,
    }

    return {
        'payload': utils.des_encrypt(json.dumps(payload), client_password),
        'ticket': utils.des_encrypt(json.dumps(ticket), auth_tgs_password),
    }


def generate_client_tgs_password():
    print('Generating password between tgs and client')
    password = str(random.randint(0, 9999))
    hashed_password = utils.generate_hash(password)
    return hashed_password


def generate_auth_service_tgs_password():
    global auth_tgs_password
    print('Generating password between me and tgs')
    password = str(random.randint(0, 9999))
    auth_tgs_password = utils.generate_hash(password)
    utils.persist_txt('auth_tgs', 'our_secret', auth_tgs_password)


def run(server_class=HTTPServer, handler_class=Handler):
    generate_auth_service_tgs_password()
    server_address = ('', 7000)
    httpd = server_class(server_address, handler_class)
    print('Auth service initialized')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
