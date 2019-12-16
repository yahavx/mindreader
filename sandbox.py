import struct

s = open("./sandbox.py", "rb")
x = 1
while x:
    token = s.read(1)
    if not token:
        print("REACHED EOF")
        break
    x = struct.unpack('s', token)
    print(x)
print("finished!")