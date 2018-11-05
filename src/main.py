
import sys
import os
import time
import threading
import requests
import random
import names
import datetime
from threading import Lock
import gibberish
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


def client_func():
    try:
        while True:
            if random.randint(0, 100) % 30 == 0:
                register()
            if random.randint(0, 100) % 3 == 0:
                edit()
            time.sleep(0.1)
    except:
        print("Unexpected error: {0}".format(sys.exc_info()))
        os._exit(1)


def register():
    print('register new user')
    r = requests.post('http://hl-course-server-service/user')
    json = r.json()
    token = json['data']['token']
    mutex.acquire()
    tokens.append(token)
    mutex.release()


def edit():
    token = rand_token()
    if token is None:
        return

    profile = dict()

    if random.randint(0, 100) % 3 == 0:
        profile['first_name'] = names.get_first_name()

    if random.randint(0, 100) % 3 == 0:
        profile['last_name'] = names.get_last_name()

    if random.randint(0, 100) % 3 == 0:
        profile['birth_date'] = random.randint(0, 1541376257)

    if random.randint(0, 100) % 3 == 0:
        profile['status'] = ' '.join(gibberish.generate_words(random.randint(3, 10)))

    print('edit user profile: {0}'.format(profile))

    r = requests.patch('http://hl-course-server-service/profile/{0}'.format(token), json=profile)
    if r.status_code != 200:
        print("can't edit user profile: {0}".format(r.text))


def rand_token():
    if len(tokens) == 0:
        return None

    mutex.acquire()
    token = tokens[random.randint(0, len(tokens)-1)]
    mutex.release()
    return token


if __name__ == '__main__':

    my_thread0 = threading.Thread(target=client_func)
    my_thread0.start()

    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    print('listening for /healthz on 0.0.0.0:8080/healthz\n')
    server.serve_forever()
