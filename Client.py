import socket
import tqdm
import os
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
    client_name = input("Enter the faculty name: ")
    ClientSocket.send(str.encode(client_name))
    Response = ClientSocket.recv(1024)
    print(f"{client_name} is connected to the server", client_name)
    print("enter the path of your faculty csv:")


except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientheSocket.close()
