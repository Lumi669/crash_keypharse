
# note: the there are two different keys, one is the guessed full-length key,
# the other one is part key.
import socket
import hmac
import hashlib


USER_NAME = b"241153"
TAG = b"ClientCmd"
COMMAND = b'a'*31
DILIMIT = b"|"



def generate_hmac(sec_key):

    total_parameter = TAG + DILIMIT + USER_NAME + DILIMIT + COMMAND + sec_key.encode("utf-8")
    generated_hmac = hmac.new(sec_key.encode("utf-8"), total_parameter, hashlib.sha256).hexdigest()

    return generated_hmac


key = 'b'*19 + 'b'
print("key = ", key)

print("key = ", key)

hmacc = generate_hmac(key)
print('hamc = ', hmacc)

HOST = 'device1.vikaa.fi'  # The server's hostname or IP address
PORT = 35984       # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    print('server connected')

    s.sendall(b'241153;' + COMMAND + key.encode("utf-8") + b';' + hmacc.encode("utf-8") + b'\n')

    print('data sent')

    data = s.recv(1024)
    print("data = ", data)

print('Received', repr(data))