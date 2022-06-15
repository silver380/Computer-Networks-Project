import os.path
import socket
import subprocess
import tqdm
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 5000
BUFFER_SIZE = 1000
ThreadCount = 0

while True:
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
        continue
    break

# Creating Clients
client_number = int(input("Enter the number of Clients:"))
print(f"[*] Listening as {host}:{port}")
ServerSocket.listen(client_number)
for i in range(client_number):
    subprocess.call(["gnome-terminal", "--", "sh", "-c", "python3 ./Client.py"])


def threaded_client(connection):
    try:
        client_name = connection.recv(1000).decode()
        print(client_name)
        data = connection.recv(BUFFER_SIZE).decode()
        file_size = int(data)
        print("size is", file_size)
        file_name = f"./{client_name}.csv"
        progress = tqdm.tqdm(range(file_size), f"Saving in {file_name}",mininterval=0.00000001, maxinterval=0.00000001, unit="B", unit_scale=True,
                             unit_divisor=2048, colour='blue')
        total_rcv = 0
        with open(file_name, "wb") as f:
            while True:
                bytes_read = connection.recv(BUFFER_SIZE)
                total_rcv += len(bytes_read)
                progress.update(len(bytes_read))
                f.write(bytes_read)
                if total_rcv >= file_size:
                    break
        connection.sendall(str.encode("saved successfully"))
        while True:
            data = connection.recv(BUFFER_SIZE).decode()
            if not data:
                break

    except socket.error as er:
        print(str(er))

    # connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()
