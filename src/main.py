
import sys
import time
import threading
import requests
from threading import Thread, Lock
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/healthz':
            self.send_response(200)
            self.send_header('X-Healthz-Header', 'Awesome')
            self.end_headers()
        return


mutex = Lock()
tokens = []


def register_client_func():
    while True:
        mutex.acquire()
        r = requests.post('http://hl-course-server-service/user')
        print(r.text)
        mutex.release()
        time.sleep(1)


def edit_client_func():
    while True:
        mutex.acquire()
        mutex.release()
        time.sleep(0.3)


if __name__ == '__main__':
    my_thread0 = threading.Thread(target=register_client_func)
    my_thread0.start()

    my_thread1 = threading.Thread(target=edit_client_func)
    my_thread1.start()

    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    print('listening for /healthz on 0.0.0.0:8080/healthz\n')
    server.serve_forever()
