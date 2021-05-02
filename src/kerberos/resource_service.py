import json
import utils
import random
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/execute_action':
            request = utils.parse_received_request(self)
            response = generate_m6(request)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), 'utf8'))

    def log_message(self, format, *args):
        pass


def generate_m6(request):
    request_ticket = get_request_ticket(request['ticket'])
    client_service_password = request_ticket['client_password']
    params = utils.get_request_params(client_service_password, request['request'])

    payload = {
        'response': execute_action(params),
    }

    return {
        'payload': utils.des_encrypt(json.dumps(payload), client_service_password),
    }


def execute_action(params):
    return params['client_id'] + ' accessed resource ' + params['resource']


def get_request_ticket(tgs_ticket):
    tgs_service_password = utils.load_file('tgs_service', 'our_secret')
    service_ticket = utils.des_decrypt(tgs_ticket, tgs_service_password)
    return json.loads(service_ticket)


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 9001)
    httpd = server_class(server_address, handler_class)
    print('Resource service 1 initialized')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
