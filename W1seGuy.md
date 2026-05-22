### Room Link: https://tryhackme.com/room/w1seguy

- Here a python script is given

- given script 
```
import random
import socketserver 
import socket, os
import string

flag = open('flag.txt','r').read().strip()

def send_message(server, message):
    enc = message.encode()
    server.send(enc)

def setup(server, key):
    flag = 'THM{thisisafakeflag}' 
    xored = ""

    for i in range(0,len(flag)):
        xored += chr(ord(flag[i]) ^ ord(key[i%len(key)]))

    hex_encoded = xored.encode().hex()
    return hex_encoded

def start(server):
    res = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    key = str(res)
    hex_encoded = setup(server, key)
    send_message(server, "This XOR encoded text has flag 1: " + hex_encoded + "\n")
    
    send_message(server,"What is the encryption key? ")
    key_answer = server.recv(4096).decode().strip()

    try:
        if key_answer == key:
            send_message(server, "Congrats! That is the correct key! Here is flag 2: " + flag + "\n")
            server.close()
        else:
            send_message(server, 'Close but no cigar' + "\n")
            server.close()
    except:
        send_message(server, "Something went wrong. Please try again. :)\n")
        server.close()

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        start(self.request)

if __name__ == '__main__':
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 1337), RequestHandler)
    server.serve_forever() 
```

- To solve the code I have to connect the machine via nc on port 1337

```
nc 10.48.167.163 1337
```

- Now I get a chipher text and by the given code I know this is the Encrypted Hex Text of the flag 

- Encrypted format : The flag is encrypted using XOR with a random 5-character key.

- ```Flag + Repeating Key + XOR = Encrypted Hex Text```

- Script to get the encryption key & first flag

```
import string
from pwn import *

charset = string.ascii_letters + string.digits

eng_flag = bytes.fromhex("053c3b101a60151a051e140c022a1e2540150009101a04580b3d380f033f23000f5b1f230c391917")

part_flag = b'THM{'

part_key = xor(eng_flag, part_flag)[:4]

# print("Key:", part_key)

for c in charset:
    key = part_key + c.encode()
    dec_flag = xor(eng_flag, key).decode()
    
    if dec_flag[-1] == '}':
        print(f"Trying key: {key} -> {dec_flag}")
        print(f"Flag: {dec_flag}")
```

- by using the encryption key i got the second flag..
