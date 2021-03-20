from http.server import BaseHTTPRequestHandler, HTTPServer
import io
from User import User, loadUser
from TokenGenerator import TokenGenerator


logged_user = None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        page = ''

        if self.path == '/signup':
            file = io.open('signup.html', mode='r', encoding='utf-8')
            page = file.read()
            file.close()

        if self.path == '/login':
            file = io.open('login.html', mode='r', encoding='utf-8')
            page = file.read()
            file.close()

        if self.path == '/token':
            token_generator = TokenGenerator(getLoggedUser().seed_password)
            page = ','.join(token_generator.getActualTokens())

        self.wfile.write(bytes(page, "utf8"))


    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        if self.path == '/signup':
            user = User(self.parse_post_request())
            user.persist()

        if self.path == '/login':
            user = loadUser(self.parse_post_request())

            if user is None:
                self.wfile.write(bytes('user nor found', "utf8"))
                return

            if user == 'wrong password':
                self.wfile.write(bytes(user, "utf8"))
                return

            setLoggedUser(user)


    def parse_post_request(self):
        content_len = int(self.headers.get('content-length', 0))
        return {param.split('=')[0]: param.split('=')[1] for param in self.rfile.read(content_len).decode('utf-8').split('&')}


def run(server_class=HTTPServer, handler_class=handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def setLoggedUser(user):
    global logged_user
    logged_user = user


def getLoggedUser():
    global logged_user
    return logged_user


if __name__ == '__main__':
    run()
