import os.path
import socket
import subprocess
import tqdm
import pandas as pd
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 5000
BUFFER_SIZE = 1000
ThreadCount = 0


# Creating Clients

def creating_clients():
    client_number = int(input("Enter the number of Clients:"))
    print(f"[*] Listening as {host}:{port}")
    ServerSocket.listen(client_number)
    for i in range(client_number):
        subprocess.call(["gnome-terminal", "--", "sh", "-c", "python3 ./Client.py"])


def threaded_client(connection):
    try:
        client_name = connection.recv(1000).decode()
        if not os.path.exists(f"./Server_CSVs/{client_name}.csv"):
            connection.send('0'.encode())
            data = connection.recv(BUFFER_SIZE).decode()
            file_size = int(data)
            file_name = f"./Server_CSVs/{client_name}.csv"
            progress = tqdm.tqdm(range(file_size), f"Saving in {file_name}", mininterval=0.00000001,
                                 maxinterval=0.00000001,
                                 unit="B", unit_scale=True, unit_divisor=2048, colour='blue')
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
        else:
            connection.send('1'.encode())
        client_df = pd.read_csv(f"./Server_CSVs/{client_name}.csv")
        client_df['Average'] = client_df.iloc[:, 4:9].mean(axis=1)
        while True:
            command = connection.recv(BUFFER_SIZE).decode()
            if command == 'Average':
                average = client_df['Average'].mean()
                connection.send(str(average).encode())
            elif command == 'Sort':
                sorted_df = client_df.copy().sort_values(by='Average', ascending=False)[['Second_ID', 'Average']]
                sorted_df.to_csv(path_or_buf=f"./Server_CSVs/Sorted_{client_name}.csv",index=False)
                try:
                    sorted_file_name = f"./Server_CSVs/Sorted_{client_name}.csv"
                    sorted_file_size = os.path.getsize(sorted_file_name)
                    connection.send(f"{sorted_file_size}".encode())
                    progress = tqdm.tqdm(range(sorted_file_size), f"Sending {sorted_file_name}", mininterval=0.000000001,
                                         maxinterval=0.000000001,
                                         unit="B", unit_scale=True, unit_divisor=2048, colour='green', delay=0)
                    total_send = 0
                    with open(sorted_file_name, "rb") as f:
                        while True:
                            # read the bytes from the file
                            bytes_read = f.read(BUFFER_SIZE)
                            total_send += len(bytes_read)
                            progress.update(len(bytes_read))
                            connection.sendall(bytes_read)
                            if total_send >= sorted_file_size:
                                # file transmitting is done
                                break
                    os.remove(sorted_file_name)
                except os.error as er:
                    print(str(er))
                    continue



    except socket.error as er:
        print(str(er))

    # connection.close()


if __name__ == '__main__':
    while True:
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
            continue
        break
    creating_clients()
    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSocket.close()
