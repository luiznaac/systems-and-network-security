from http.server import BaseHTTPRequestHandler, HTTPServer
import io
from UserToken import UserToken


logged_user = None
error_messages = []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        page = ''

        if self.path == '/':
            file = io.open('pages/app/login.html', mode='r', encoding='utf-8')
            page = file.read().replace(':message', getErrorMessages())
            file.close()

        if self.path.replace('?', '') == '/login':
            file = io.open('pages/app/login.html', mode='r', encoding='utf-8')
            page = file.read().replace(':message', getErrorMessages())
            file.close()

        if self.path.replace('?', '') == '/app':
            file = io.open('pages/app/app.html', mode='r', encoding='utf-8')
            page = file.read()
            file.close()

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(page, "utf8"))


    def do_POST(self):
        if self.path == '/login':
            token_validation = UserToken(self.parse_post_request()).validate()

            if token_validation:
                self.send_response(303)
                self.send_header('Location', 'http://localhost:7000/app')
                self.end_headers()
                return

            if not token_validation:
                setErrorMessage('Invalid token')
                self.send_response(303)
                self.send_header('Location', 'http://localhost:7000/login')
                self.end_headers()
                return

            setErrorMessage('User not found')
            self.send_response(303)
            self.send_header('Location', 'http://localhost:7000/login')
            self.end_headers()
            return


    def parse_post_request(self):
        content_len = int(self.headers.get('content-length', 0))
        return {param.split('=')[0]: param.split('=')[1] for param in self.rfile.read(content_len).decode('utf-8').split('&')}


def run(server_class=HTTPServer, handler_class=handler):
    server_address = ('', 7000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def setErrorMessage(message):
    error_messages.append(message)


def getErrorMessages():
    messages = ','.join(error_messages)
    error_messages.clear()
    return messages


if __name__ == '__main__':
    run()
