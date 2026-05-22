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