import socket
import tqdm
import os
import sys

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 5000
BUFFER_SIZE = 10000


def send_file_info():
    while True:
        try:
            file_name = input("enter the path and name of your faculty csv:\n")
            file_size = os.path.getsize(file_name)
            ClientSocket.send(f"{file_size}".encode())
            progress = tqdm.tqdm(range(file_size), f"Sending {file_name}", mininterval=0.000000001,
                                 maxinterval=0.000000001,
                                 unit="B", unit_scale=True, unit_divisor=2048, colour='blue', delay=0)
            total_send = 0
            with open(file_name, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    total_send += len(bytes_read)
                    progress.update(len(bytes_read))
                    ClientSocket.sendall(bytes_read)
                    if total_send >= file_size:
                        # file transmitting is done
                        break
            massage = ClientSocket.recv(BUFFER_SIZE).decode()
            print(massage)
        except os.error as er:
            print(str(er))
            continue
        break


def send_command():
    while True:
        os.system('clear')
        command = input("Enter your command or enter help to see available commands:\n")
        os.system('clear')
        if command == "help":
            print("you can use these commands to interact with the server:\n")
            print("[*]Done: will close the connection\n")
            print("[*]Average: See the average point of your faculty\n")
            print("[*]Sort: See the list of your Students, sorted by their average\n")
            print("[*]Max: See the first name and the last name of the student with the highest average\n")
            print("[*]Min: See the first name and the last name of the student with the lowest average\n")
            print("[*]Insert: add a new Student\n")
            input("Press enter to go back")
        if command == 'Average':
            ClientSocket.send(command.encode())
            data = ClientSocket.recv(100)
            print(f"{client_name} Students Average is: ", data.decode())
            input("press Enter to go back to main menu")
        elif command == 'Sort':
            ClientSocket.send(command.encode())
            data = ClientSocket.recv(BUFFER_SIZE).decode()
            sorted_file_size = int(data)
            sorted_file_name = f"./Client_CSVs/Sorted_{client_name}.csv"
            progress = tqdm.tqdm(range(sorted_file_size), f"Saving in {sorted_file_name}", mininterval=0.00000001,
                                 maxinterval=0.00000001,
                                 unit="B", unit_scale=True, unit_divisor=2048, colour='green')
            total_rcv = 0
            with open(sorted_file_name, "wb") as f:
                while True:
                    bytes_read = ClientSocket.recv(BUFFER_SIZE)
                    total_rcv += len(bytes_read)
                    progress.update(len(bytes_read))
                    f.write(bytes_read)
                    if total_rcv >= sorted_file_size:
                        break
            print(f"you can see the result in {sorted_file_name}")
            input("press Enter to go back to main menu")




# while True:
#     Input = input('Say Something: ')
#     ClientSocket.send(str.encode(Input))
#     Response = ClientSocket.recv(1024)
#     print(Response.decode('utf-8'))
#
# ClientheSocket.close()

if __name__ == '__main__':
    print("Welcome")
    # connecting to server
    try:
        print(f"[+] Connecting to {host}:{port}")
        ClientSocket.connect((host, port))
        print("[+] Connected.")
        client_name = input("Enter the faculty name: ")
        ClientSocket.send(str.encode(client_name))
        is_exist = int(ClientSocket.recv(4).decode())
    except socket.error as e:
        print(str(e))
        sys.exit()
    if not is_exist:
        send_file_info()
        os.system('clear')
        send_command()
    else:
        send_command()
