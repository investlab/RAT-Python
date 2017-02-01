import socket
import sys
import os

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def pad(s):
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)

def bytestring_to_int(bytes):
    i = 0
    while bytes:
        i = i << 8
        i+= ord(bytes[-1])
        bytes = bytes[:-1]
    return i
    
def int_to_bytestring(i):
    bs = ''
    while i:
        bs += chr(i & 0xff)
        i = i >> 8
    return bs
    
def encrypt(plaintext, KEY):
    plaintext = pad(plaintext)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)


def decrypt(ciphertext, KEY):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b'\0')

def diffiehellman(sock):
    # currently trying to compress this line.
    # using RFC 3526 MOPD group 14 (2048 bits)
    p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF;
    g = 2;
    a = bytestring_to_int(os.urandom(32)) # a 256bit number, sufficiently large
    xA = pow(g,a,p)
    b = bytestring_to_int(sock.recv(4096))  # order of send and recv swapped
    sock.send(int_to_bytestring(xA))        # for proper communication flow
    s = pow(xA,b,p)
    return SHA256.new(int_to_bytestring(s)).digest()
