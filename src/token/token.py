from http.server import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint
import io
import json
from User import User


USERNAME = 1
USERKEY = 2
INPUTTEXT = 3

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == '/login':
            file = io.open('login.html', mode='r', encoding='utf-8')
            login_page = file.read()
            file.close()
            self.wfile.write(bytes(login_page, "utf8"))
            return

        message = "Ok"
        self.wfile.write(bytes(message, "utf8"))


    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        if self.path == '/login':
            user = User(self.parse_post_request())
            user.persist()

        self.wfile.write(bytes('ok', "utf8"))


    def parse_post_request(self):
        content_len = int(self.headers.get('content-length', 0))
        return {param.split('=')[0]: param.split('=')[1] for param in self.rfile.read(content_len).decode('utf-8').split('&')}


def run(server_class=HTTPServer, handler_class=handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
