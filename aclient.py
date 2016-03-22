from _ssl import PROTOCOL_SSLv3
import os
import socket
import ssl

from messages import ADMIN_GREET, WHO, HELLO


HOST = "localhost"
PORT = 4001
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

cur_dir = os.getcwd()
key_file = os.path.join(cur_dir + "\\Certificate\\", '100189688.key')
cert_file = os.path.join(cur_dir + "\\Certificate\\", '100189688.crt')

# ts = ssl.wrap_socket(sock, certfile=cert_file, keyfile=key_file,
#                      server_side=False, cert_reqs=ssl.CERT_REQUIRED,ssl_version=PROTOCOL_SSLv3)

sock.sendall(HELLO)
data = sock.recv(BUFFER_SIZE)

if data == ADMIN_GREET:
    sock.sendall(WHO)
    data = sock.recv(BUFFER_SIZE)
    print data
    raw_input("Press Enter to quit...")
