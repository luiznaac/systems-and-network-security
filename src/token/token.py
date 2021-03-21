from http.server import BaseHTTPRequestHandler, HTTPServer
import io
from User import User, loadUser
from TokenGenerator import TokenGenerator


logged_user = None
error_messages = []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        page = ''

        if self.path == '/signup':
            if getLoggedUser() is not None:
                self.send_response(303)
                self.send_header('Location', 'http://localhost:8000/token')
                self.end_headers()
                return
            file = io.open('signup.html', mode='r', encoding='utf-8')
            page = file.read()
            file.close()

        if self.path == '/login':
            if getLoggedUser() is not None:
                self.send_response(303)
                self.send_header('Location', 'http://localhost:8000/token')
                self.end_headers()
                return
            file = io.open('login.html', mode='r', encoding='utf-8')
            page = file.read().replace(':message', getErrorMessages())
            file.close()

        if self.path == '/token':
            if getLoggedUser() is None:
                self.send_response(303)
                self.send_header('Location', 'http://localhost:8000/login')
                self.end_headers()
                return
            token_generator = TokenGenerator(getLoggedUser().seed_password)
            tokens = '<br>'.join(token_generator.getActualTokens())
            file = io.open('tokens.html', mode='r', encoding='utf-8')
            page = file.read()
            file.close()
            page = page.replace(':tokens', tokens)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(page, "utf8"))


    def do_POST(self):
        if self.path == '/signup':
            user = User(self.parse_post_request())
            user.persist()

        if self.path == '/login':
            user = loadUser(self.parse_post_request())

            if user is None:
                setErrorMessage('User not found')
                self.send_response(303)
                self.send_header('Location', 'http://localhost:8000/login')
                self.end_headers()
                return

            if user == 'wrong password':
                setErrorMessage('Wrong password')
                self.send_response(303)
                self.send_header('Location', 'http://localhost:8000/login')
                self.end_headers()
                return

            setLoggedUser(user)
            self.send_response(303)
            self.send_header('Location', 'http://localhost:8000/token')
            self.end_headers()


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


def setErrorMessage(message):
    error_messages.append(message)


def getErrorMessages():
    messages = ','.join(error_messages)
    error_messages.clear()
    return messages


if __name__ == '__main__':
    run()
