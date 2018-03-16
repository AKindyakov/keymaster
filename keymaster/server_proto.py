#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
1. Проверить права на файл, если они не r-- то падать ошибкой
2. Демонизироваться
"""

import json
import os
import socket
import sys

server_address = './uds_socket'


# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise


# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# if master
# Bind the socket to the port
print('starting up on %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

try:
    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from %r' % client_address)
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(2048)
                if data:
                    print('received %r' % data)
                    req = json.loads(
                        data.decode('utf-8')
                    )
                    print('command')
                    if req['command'] == 'shutdown':
                        raise SystemExit(0)
                    else:
                        connection.sendall(
                            '{"responce": "123"}'.encode('utf-8')
                        )
                else:
                    print('no more data from %r' % client_address)
                    break
        finally:
            print('Clean up the connection')
            # Clean up the connection
            connection.close()
finally:
    print('Clean up')
    os.unlink(server_address)
