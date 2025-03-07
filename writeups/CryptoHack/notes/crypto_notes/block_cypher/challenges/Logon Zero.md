We have a challenge that mimics an authentication server. It generates a random password of 16 bytes and a random key, used later for encryption operations.
```python
#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom
from utils import listener

FLAG = "crypto{???????????????????????????????}"


class CFB8:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        IV = urandom(16)
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct = b""
        state = IV
        for i in range(len(plaintext)):
            b = cipher.encrypt(state)[0]
            c = b ^ plaintext[i]
            ct += bytes([c])
            state = state[1:] + bytes([c])
        return IV + ct

    def decrypt(self, ciphertext):
        IV = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = b""
        state = IV
        for i in range(len(ct)):
            b = cipher.encrypt(state)[0]
            c = b ^ ct[i]
            pt += bytes([c])
            state = state[1:] + bytes([ct[i]])
        return pt


class Challenge:
    def __init__(self):
        self.before_input = "Please authenticate to this Domain Controller to proceed\n"
        self.password = urandom(20)
        self.password_length = len(self.password)
        self.cipher = CFB8(urandom(16))

    def challenge(self, your_input):
        if your_input["option"] == "authenticate":
            if "password" not in your_input:
                return {"msg": "No password provided."}
            your_password = your_input["password"]
            if your_password.encode() == self.password:
                self.exit = True
                return {"msg": "Welcome admin, flag: " + FLAG}
            else:
                return {"msg": "Wrong password."}

        if your_input["option"] == "reset_connection":
            self.cipher = CFB8(urandom(16))
            return {"msg": "Connection has been reset."}

        if your_input["option"] == "reset_password":
            if "token" not in your_input:
                return {"msg": "No token provided."}
            token_ct = bytes.fromhex(your_input["token"])
            if len(token_ct) < 28:
                return {"msg": "New password should be at least 8-characters long."}

            token = self.cipher.decrypt(token_ct)
            new_password = token[:-4]
            self.password_length = bytes_to_long(token[-4:])
            self.password = new_password[: self.password_length]
            return {"msg": "Password has been correctly reset."}


import builtins

builtins.Challenge = Challenge  # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13399)
```

Note that we have the possibility of changing our password if we are able to supply a text that can be decrypted successfully. Because of the fact that the last 4 bytes are also used to determine the password length, if we managed to obtain any ciphertext whose last bytes are all `0`, we could supply an empty password and login.

The mode of operation used by the server to decrypt our message is `CFB-8`, which is a variant of the [CFB mode of operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CFB-1,_CFB-8,_CFB-64,_CFB-128,_etc.). This mode of operation came to prominence when [CVE-2020-1472](https://www.secura.com/uploads/whitepapers/Zerologon.pdf) was released, and the reason was that `CFB-8` was used in Windows' Active Directory service to authenticate users. A researcher found that, because of this mode of operation, if the IV is not properly random it is possible to produce a ciphertext that consists of all zeros:

![](https://i.imgur.com/pE9Em64.png)

In order to solve the challenge we just need to send a message with 28 0 bytes:
```python
#!/usr/bin/env python

from pwn import *
import json


attack_token = b"\x00" * 28

c = remote("socket.cryptohack.org", 13399)
i = 0
c.recvline()
while True:
    print("Try:", i, end="\r")
    c.sendline(
        json.dumps({"option": "reset_password", "token": attack_token.hex()}).encode()
    )
    c.recvline()

    c.sendline(json.dumps({"option": "authenticate", "password": ""}).encode())
    text = c.recvline()
    if b"admin" in text:
        print("Flag:", json.loads(text)["msg"])
        break
    c.sendline(json.dumps({"option": "reset_connection"}).encode())
    c.recvline()
    i += 1
```

Flag: `crypto{Zerologon_Windows_CVE-2020-1472}`