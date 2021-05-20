import socket
import io
from threading import Thread

CRLF = '\r\n\r\n'


def run():
    s = socket.socket()
    s.bind(('', 8081))
    s.listen(1000)

    while True:
        c, addr = s.accept()
        client_thread = Thread(target=handle_connection, args=(c,))
        client_thread.start()


def handle_connection(c):
    try:
        received_request = c.recv(8192)

        if 'monitorando' in str(received_request, 'utf8'):
            send_monitorando_response(c)
            return

        make_request_and_return_to_client(c, received_request)
    except Exception as e:
        print(e)
        pass
    finally:
        try:
            c.close()
        except:
            pass


def send_monitorando_response(c):
    file = io.open('monitorando.html', mode='r', encoding='utf-8')
    page = file.read()
    file.close()

    response = "HTTP/1.1 200 OK" \
               "Content-Length: " + str(len(page)) + \
               "Content-Type: text/html; charset=utf-8" \
               "Connection: Closed" \
               + CRLF \
               + page

    c.send(bytes(response, 'utf8'))


def make_request_and_return_to_client(c, received_request):
    [host, port] = get_host_and_port(received_request)

    received_data = b''
    requested_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requested_socket.connect((host, port or 80))
    requested_socket.send(bytes(prepare_request(received_request), 'utf8'))
    while True:
        data = requested_socket.recv(4194304)
        if data:
            c.send(data)
            received_data += data
            continue
        break

    print(c.getpeername(), end='')
    print(' -> ', end='')
    print(requested_socket.getpeername())
    requested_socket.close()


def prepare_request(received_request):
    received_request = received_request.decode('utf8')
    return received_request.rstrip(CRLF) + '\r\nConnection: close' + CRLF


def get_host_and_port(received_request):
    host = get_host(received_request)
    port = get_port_if_exists(host)

    host = host if not port else host.split(':')[0]

    return [host, port]


def get_port_if_exists(host):
    if host and ':' in host:
        split_host = host.split(':')
        return int(split_host[1])
    return None


def get_host(request):
    split_request = request.decode('utf8').split('\r\n')

    for header in split_request:
        if len(header) > 0:
            split_header = header.split(': ')
            if split_header[0] == 'Host':
                return split_header[1]


if __name__ == '__main__':
    run()
