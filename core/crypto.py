# -*- coding: utf-8 -*-

#
# basicRAT crypto module
# https://github.com/vesche/basicRAT
#

import os
import socket

from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long, long_to_bytes
from aes_gcm import *


FB_KEY = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"


class PaddingError(Exception):
    pass


# PKCS#7 - RFC 2315 section 10.3.2
def pkcs7(s, bs=16):
    i = (bs - (len(s) % bs))
    return s + (chr(i)*i)


# Strip PKCS#7 padding - throws PaddingError on failure
def unpkcs7(s):
    i = s[-1]
    if s.endswith(i*ord(i)):
        return s[:-ord(i)]
    raise PaddingError("PKCS7 improper padding {}".format(repr(s[-32:])))


# Diffie-Hellman Internet Key Exchange (IKE) - RFC 2631
def diffiehellman(sock, server=True, bits=2048):
    # using RFC 3526 MOPD group 14 (2048 bits)
    p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF;
    g = 2
    a = bytes_to_long(os.urandom(32)) # a 256bit number, sufficiently large
    xA = pow(g, a, p)

    if server:
        sock.send(long_to_bytes(xA))
        b = bytes_to_long(sock.recv(4096))
    else:
        b = bytes_to_long(sock.recv(4096))
        sock.send(long_to_bytes(xA))

    s = pow(b, a, p)
    return SHA256.new(long_to_bytes(s)).digest()


# take plaintext, encrypt using GCM object, and send over sock
def sendGCM(sock, GCM_obj, IV, plaintext):
    ciphertext, tag = GCM_obj.encrypt(IV, plaintext)
    return sock.send(long_to_bytes(IV, 12) + ciphertext + long_to_bytes(tag, 16))


# read data from sock, decrypt using gcm object, and return plaintext
# WARNING: gcm.decrypt throws InvalidTagException upon tampered/corrupted
# this will need to be handled outside of this function
def recvGCM(sock, GCM_obj):
    m = ''
    while True:
        try:
            m += sock.recv(4096)
        except socket.error:
            break

    # prevents decryption of empty string
    if not m:
        return m

    IV = bytes_to_long(m[:12])
    ciphertext = m[12:-16]
    tag = bytes_to_long(m[-16:])

    return GCM_obj.decrypt(IV, ciphertext, tag)