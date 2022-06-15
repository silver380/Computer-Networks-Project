import socket
import tqdm
import os
import pandas
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 5000
BUFFER_SIZE = 10000  # send 5000 bytes each time step
print('Waiting for connection')

try:
    print(f"[+] Connecting to {host}:{port}")
    ClientSocket.connect((host, port))
    print("[+] Connected.")
    client_name = input("Enter the faculty name: ")
    ClientSocket.send(str.encode(client_name))
    print(f"{client_name} is connected to the server", client_name)
except socket.error as e:
    print(str(e))

while True:
    try:
        file_name = input("enter the path and name of your faculty csv:\n")
        file_size = os.path.getsize(file_name)
        ClientSocket.send(f"{file_size}".encode())
        progress = tqdm.tqdm(range(file_size), f"Sending {file_name}",mininterval=0.000000001, maxinterval=0.000000001, unit="B", unit_scale=True,
                             unit_divisor=2048, colour='blue')
        total_send = 0
        with open(file_name, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                total_send += len(bytes_read)
                progress.update(len(bytes_read))
                ClientSocket.sendall(bytes_read)
                if total_send >= file_size:
                    print("ok")
                    # file transmitting is done
                    break
        massage = ClientSocket.recv(BUFFER_SIZE).decode()
        print(massage)

    except os.error as e:
        print(str(e))
        continue
    break

while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientheSocket.close()
