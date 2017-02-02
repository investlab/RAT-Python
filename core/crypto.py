# -*- coding: utf-8 -*-

#
# basicRAT crypto module
# https://github.com/vesche/basicRAT
#

from Crypto import Random
from Crypto.Cipher import AES


KEY  = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"


def AES_pad(s):
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)


def AES_encrypt(plaintext):
    plaintext = AES_pad(plaintext)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)


def AES_decrypt(ciphertext):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b'\0')
