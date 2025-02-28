In this chall we have a server that performs `AES` encryption in `CTR` mode, in a way that does not seem to be vulnerable:
```python
from Crypto.Cipher import AES
from Crypto.Util import Counter
import zlib


KEY = ?
FLAG = ?


@chal.route('/ctrime/encrypt/<plaintext>/')
def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)

    iv = int.from_bytes(os.urandom(16), 'big')
    cipher = AES.new(KEY, AES.MODE_CTR, counter=Counter.new(128, initial_value=iv))
    encrypted = cipher.encrypt(zlib.compress(plaintext + FLAG.encode()))

    return {"ciphertext": encrypted.hex()}
```

However, we can notice that the text being encrypted is appended in front of the flag, and then *compressed*. Because of how compression works, we can use this as an oracle. We know that the flag starts with `crypto{`, and sending a plaintext `crypto{x`, where $x$ is a char that is not part of the flag, we can see that we obtain a text longer than the `crypto{` ciphertext. This is relevant because we can obtain a similar result sending a string like `crxpto{`.

This is because the compression shortens the final text to be encrypted, and as a result the final ciphertext will be shorter to if we append a string that is a substring of the flag. We can bruteforce the flag one character at a time:
```python
#!/usr/bin/env python

import requests
import string


ENDPOINT = "https://aes.cryptohack.org/ctrime/encrypt/%s"


flag = b"crypto{CRIME_571ll_p4y5}"
base_len = len(
    bytes.fromhex(
        requests.get(ENDPOINT % ((flag + b"}") * 2).hex()).json()["ciphertext"]
    )
)

while flag[-1] != ord("}"):
    for candidate in string.printable:
        encrypted = bytes.fromhex(
            requests.get(ENDPOINT % ((flag + candidate.encode()) * 2).hex()).json()[
                "ciphertext"
            ]
        )
        print("[+] Trying: %s" % (flag + candidate.encode()), len(encrypted), end="\r")
        if len(encrypted) < base_len:
            flag += candidate.encode()
            print("Found:", flag.decode())
            break
    else:
        print("[-] Not found")
        break
```

The `*2` is necessary because the script breaks at a certain point. Doubling the prefix string solves this problem.