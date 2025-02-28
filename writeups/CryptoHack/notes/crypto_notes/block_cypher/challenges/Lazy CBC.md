In this challenge we have a server that allows us to encrypt text in CBC mode, but we know that $IV = Key$:
```python
from Crypto.Cipher import AES


KEY = ?
FLAG = ?


@chal.route('/lazy_cbc/encrypt/<plaintext>/')
def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)
    if len(plaintext) % 16 != 0:
        return {"error": "Data length must be multiple of 16"}

    cipher = AES.new(KEY, AES.MODE_CBC, KEY)
    encrypted = cipher.encrypt(plaintext)

    return {"ciphertext": encrypted.hex()}


@chal.route('/lazy_cbc/get_flag/<key>/')
def get_flag(key):
    key = bytes.fromhex(key)

    if key == KEY:
        return {"plaintext": FLAG.encode().hex()}
    else:
        return {"error": "invalid key"}


@chal.route('/lazy_cbc/receive/<ciphertext>/')
def receive(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)
    if len(ciphertext) % 16 != 0:
        return {"error": "Data length must be multiple of 16"}

    cipher = AES.new(KEY, AES.MODE_CBC, KEY)
    decrypted = cipher.decrypt(ciphertext)

    try:
        decrypted.decode() # ensure plaintext is valid ascii
    except UnicodeDecodeError:
        return {"error": "Invalid plaintext: " + decrypted.hex()}

    return {"success": "Your message has been received"}

```

In order to understand how to exploit this vulnerability, we need to look at how CBC decryption is made. Suppose that we have a plaintext of three blocks:
$$
P = \begin{cases}
P_0 = IV \oplus D_k(C_0) \\
P_1 = C_0 \oplus D_k(C_1) \\
P_2 = C_1 \oplus D_k(C_2) \\
\end{cases}
$$

An attacker could tamper the ciphertext to have:
$$
C_0 = C_0, C_1 = 0, C_2 = C_0
$$
And this way, the decryption becomes:
$$
P = \begin{cases}
P_0 = IV \oplus D_k(C_0) \\
P_1 = C_0 \oplus D_k(0) \\
P_2 = 0 \oplus D_k(C_0) \\
\end{cases}
$$

This way `XOR`ing $P_0 \oplus P_2$ gives:
$$
P_0 \oplus P_2 = IV \oplus D_K(C_0) \oplus D_K(C_0) \oplus 0 = IV = Key
$$
Solution described [here](https://crypto.stackexchange.com/a/67231)

An alternative solution would require an attacker to send a ciphertext of two blocks, both at $0$. This way we have
$$
P = \begin{cases}P_0 = IV \oplus D_k(0) \\ 
P_1 = 0 \oplus D_k(0)
\end{cases}
$$

now `XOR`ing $P_0 \oplus P_1$ gives:
$$
P_0 \oplus P_1= IV \oplus 0 \oplus D_k(0) \oplus D_k(0) = IV = Key
$$