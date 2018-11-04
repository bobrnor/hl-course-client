
import sys
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('X-Healthz-Header', 'Awesome')
            self.end_headers()
        return


def client_func():
    iteration = 0
    while True:
        sys.stderr.write('client iteration #{0}\n'.format(iteration))
        iteration += 1
        time.sleep(5)


if __name__ == '__main__':
    my_thread = threading.Thread(target=client_func)
    my_thread.start()

    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    sys.stderr.write('listening for /healthz on 0.0.0.0:8080/healthz\n')
    server.serve_forever()
