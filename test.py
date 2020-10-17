

a = [b'N', b'k', b'5', b'2', b'D', b'l', b'c', b'K', b'9', b'4', b'r', b'O', b't', b'e', b'Z', b'O', b'0', b'V', b'V']
a.reverse()

a_string = ""
for item in a:
    a_string += item.decode("latin-1")

print(a)


print(a_string)
# b'\xffVV0OZetOr49KclD25kN'

c = b'|VV0OZetOr49KclD25kN'

print("c = ", c.decode("latin-1"))