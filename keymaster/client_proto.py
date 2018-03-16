#!/usr/bin/env python3

import json
import socket
import sys

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening

server_address = './uds_socket'
print('connecting to %r' % server_address)

try:
    sock.connect(server_address)
except socket.error as err:
    print("%r" % err)
    sys.exit(1)

try:
    # Send data
    message = {
        "command": "req"
    }
    print('sending "%s"' % message)
    sock.sendall(
        json.dumps(message).encode('utf-8')
    )

    amount_received = 0
    amount_expected = len(message)

    data = sock.recv(2048)
    print('received "%r"' % data)

finally:
    print('closing socket')
    sock.close()
