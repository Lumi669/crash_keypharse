import hmac
import hashlib


#
# USER_NAME = b"241153"
# tag = b"ClientCmd"
# secret_key = b"bbbbbbbbbbbbbbbbbbbb"
# command = b'a'*31
# command_and_key = command + secret_key
# delim = b"|"
#
#
# total_parameter = tag + delim + USER_NAME + delim + command_and_key
#
# print(total_parameter)
# print(secret_key)
# resulted_hmac = hmac.new(secret_key, total_parameter, hashlib.sha256).hexdigest()
#
# # print("resulted_hmac = {0}".format(resulted_hmac))
# print("resulted_hamc = ", resulted_hmac)

USER_NAME = b"241153"
TAG = b"ClientCmd"
COMMAND = b'a'*31
DILIMIT = b"|"

def generate_hmac(sec_key):

    total_parameter = TAG + DILIMIT + USER_NAME + DILIMIT + COMMAND + sec_key.encode("utf-8")
    generated_hmac = hmac.new(sec_key.encode("utf-8"), total_parameter, hashlib.sha256).hexdigest()

    return generated_hmac

output_hmac = generate_hmac('b'*20)
print(output_hmac)



