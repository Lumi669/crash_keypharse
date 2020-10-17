#!/usr/bin/env python3

import socket
# import time

hmac = b"a" * 64



HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # time.sleep(1)
    print('server connected')
    s.sendall(b'241153;comeon;' + hmac + b'\n')
    # s.sendall(b'ag;45435;1235114\n')
    print('data sent')

    data = s.recv(1024)

print('Received', repr(data))