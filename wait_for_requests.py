import socket

from model import main

HOST = '127.0.0.1'
PORT = 8080

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
conn, addr = s.accept()

print('Connected by', addr)

# start training process now that connection is established
print('training started')
main()

while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)
