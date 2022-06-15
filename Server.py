import os.path
import socket
import subprocess
import sqlite3
import tqdm
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
BUFFER_SIZE = 10000
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
        client_name = connection.recv(BUFFER_SIZE).decode()
        print(client_name)
        getting_file = True
        while getting_file:
            data = connection.recv(BUFFER_SIZE).decode()
            if not data:
                break
            file_size = int(data)
            print("size is", file_size)
            file_name = os.path.basename(f"./{client_name}.csv")
            progress = tqdm.tqdm(range(file_size), f"Saving in {file_name}", unit="B", unit_scale=True,
                                 unit_divisor=2048)
            total_rcv = 0
            with open(file_name, "wb") as f:
                while True:
                    bytes_read = connection.recv(BUFFER_SIZE)
                    total_rcv += len(bytes_read)
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
                    if total_rcv >= file_size:
                        # nothing is received
                        # file transmitting is done
                        getting_file = False
                        break
                    # write to the file the bytes we just received
            print("ok")
            connection.sendall(str.encode("saved successfully"))
    except socket.error as er:
        print(str(er))
    connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

ServerSocket.close()
