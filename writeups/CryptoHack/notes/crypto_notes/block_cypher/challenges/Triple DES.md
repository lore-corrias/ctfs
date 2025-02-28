This challenge consist of a server that encrypts the flag for a given key, and allows also for encrypting a custom plaintext with a custom key:
```python
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad


IV = os.urandom(8)
FLAG = ?


def xor(a, b):
    # xor 2 bytestrings, repeating the 2nd one if necessary
    return bytes(x ^ y for x,y in zip(a, b * (1 + len(a) // len(b))))



@chal.route('/triple_des/encrypt/<key>/<plaintext>/')
def encrypt(key, plaintext):
    try:
        key = bytes.fromhex(key)
        plaintext = bytes.fromhex(plaintext)
        plaintext = xor(plaintext, IV)

        cipher = DES3.new(key, DES3.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext)
        ciphertext = xor(ciphertext, IV)

        return {"ciphertext": ciphertext.hex()}

    except ValueError as e:
        return {"error": str(e)}


@chal.route('/triple_des/encrypt_flag/<key>/')
def encrypt_flag(key):
    return encrypt(key, pad(FLAG.encode(), 8).hex())
```

The encryption is not made with `AES` but [DES](https://en.wikipedia.org/wiki/Data_Encryption_Standard), a legacy encryption scheme that is considered by many the parent of block ciphers, and because of this it has been deprecated, since it is not deemed secure anymore (due to the fact that the key can be easily bruteforced).

The vulnerability, in this case, lies in the fact that we are able to perform an encryption with a custom key, and this encryption scheme is known to have some serious vulnerability for any given [weak key](https://en.wikipedia.org/wiki/Weak_key). A weak key is a key which degenerates the cipher in a way that makes the encryption function *symmetrical*. 

In order to solve the challenge, we can encrypt the flag with a weak key, like, for example:
$$
key = 0x0000000000000000
$$
This is a weak key for standard `DES`, but the server uses [Triple DES](https://en.wikipedia.org/wiki/Triple_DES), which tries to balance common `DES` vulnerability by applying the encryption three times. Since the base standard is the same, `TDES` is also vulnerable to weak keys, but this mode of operation of double/triple the size (since it has to split the key in 3 parts to perform `DES` multiple times). Providing a key like $key = 00000000000000000000000000000000$ does not work, because this would make $key_1 = key_2 = key_3$ and degenerate `TDES` to standard `DES`, raising an exception in the process. We can instead combine two different weak keys to obtain the same result, for example:
$$
key = 0x0000000000000000FFFFFFFFFFFFFFFF
$$
Now we make the server calculate
$$
enc\_flag = Enc_{key}(flag)
$$
and perform the flag by running through the encryption again:
$$
flag = Enc_{key}(Enc_{key}(flag))
$$
