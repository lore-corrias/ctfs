The challenge is very simple: we are given a function that randomly encrypts a plaintext $p$, extracted randomly from an array of an unknown length:
```python
from Crypto.Cipher import AES
from Crypto.Util import Counter
import random


KEY = ?
TEXT = ['???', '???', ..., FLAG]


@chal.route('/stream_consciousness/encrypt/')
def encrypt():
    random_line = random.choice(TEXT)

    cipher = AES.new(KEY, AES.MODE_CTR, counter=Counter.new(128))
    encrypted = cipher.encrypt(random_line.encode())

    return {"ciphertext": encrypted.hex()}

```

The main vulnerability here is that no matter the plaintext, the encryption is performed using the *same key*, because the cipher is initialized at every call, but the key isn't. 

This basically means that, because of the `CRT` mode of operation, the encryption becomes something like:
$$
messages = \begin{cases}Enc(m_1) = m_1 \oplus K \\ Enc(m_2) = m_2 \oplus K
\\...\\
Enc(m_n) = m_n \oplus K
\end{cases}
$$
This degenerates `AES` into an easier to break encryption scheme, known as Multi Time Pad (this is actually the name of the attack, the encryption scheme is itself a [One Time Pad](https://en.wikipedia.org/wiki/One-time_pad), where the pad is reused $n$ times).

The vulnerability in this kind of attack is that if $m$ is a message in, say, common english, it is possible to retrieve the messages by trying different combinations until the result of the `XOR`s eventually produce an understandable text. A tool to perform this kind of attack is [MTP](https://github.com/CameronLonsdale/MTP), and [here](https://asciinema.org/a/204705) is a demonstration of how it works.

In order to solve the challenge, we just need to dump every ciphertext and then run MTP:
```python
#!/usr/bin/env python

import requests
import os


ENCRYPT_ENDPOINT = "https://aes.cryptohack.org/stream_consciousness/encrypt/"


def get_ciphertexts():
    texts = []
    print("[+] Getting 22 unique ciphertexts from website.")
    i = 0
    while len(texts) < 22:
        text = requests.get(ENCRYPT_ENDPOINT).json()["ciphertext"]
        if text not in texts:
            texts.append(text)
        i += 1
    print("[+] Got 22 unique ciphertexts. Took {} requests".format(i))
    return texts


ciphertexts = []
if not os.path.exists("ciphertexts"):
    with open("ciphertexts", "w") as f:
        ciphertexts = get_ciphertexts()
        f.writelines([x + "\n" for x in ciphertexts])
```

The command to run the tool is `mtp ciphertexts`:
![[Pasted image 20241106212620.png]]