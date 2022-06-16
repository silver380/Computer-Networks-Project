import socket
import tqdm
import os
import sys
import pickle
import pandas as pd

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 4000
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
            print("[*]Done: close the connection\n")
            print("[*]Average: See the average point of your Students\n")
            print("[*]Sort: See the list of your Students, sorted by their average\n")
            print("[*]Max: See the first name and the last name of the student with the highest average\n")
            print("[*]Min: See the first name and the last name of the student with the lowest average\n")
            print("[*]Insert: add a new Student\n")
            input("Press enter to go back")
        if command == 'Average':
            ClientSocket.send(command.encode())
            data = ClientSocket.recv(BUFFER_SIZE).decode()
            averaged_file_size = int(data)
            averaged_file_name = f"./Client_CSVs/Averged_{client_name}.csv"
            progress = tqdm.tqdm(range(averaged_file_size), f"Saving in {averaged_file_name}", mininterval=0.00000001,
                                 maxinterval=0.00000001,
                                 unit="B", unit_scale=True, unit_divisor=2048, colour='red')
            total_rcv = 0
            with open(averaged_file_name, "wb") as f:
                while True:
                    bytes_read = ClientSocket.recv(BUFFER_SIZE)
                    total_rcv += len(bytes_read)
                    progress.update(len(bytes_read))
                    f.write(bytes_read)
                    if total_rcv >= averaged_file_size:
                        break
            average_df = pd.read_csv(averaged_file_name)
            print(average_df)
            print(f"you can see the result in {averaged_file_name}")
            input("press Enter to go back to main menu")
            os.system('clear')
            continue
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
            sorted_df = pd.read_csv(sorted_file_name)
            print(sorted_df)
            print(f"you can see the result in {sorted_file_name}")
            input("press Enter to go back to main menu")
            os.system('clear')
            continue
        elif command == 'Max':
            ClientSocket.send(command.encode())
            data = ClientSocket.recv(BUFFER_SIZE)
            data = pickle.loads(data)
            print(f"{data[0]} {data[1]} with average {data[2]} has the highest average in your faculty")
            input("press Enter to go back to main menu")
            os.system('clear')
            continue
        elif command == 'Min':
            ClientSocket.send(command.encode())
            data = ClientSocket.recv(BUFFER_SIZE)
            data = pickle.loads(data)
            print(f"{data[0]} {data[1]} with average {data[2]} has the lowest average in your faculty")
            input("press Enter to go back to main menu")
            os.system('clear')
            continue
        elif command == 'Insert':
            new_data = []
            id = input("enter the student ID:\n")
            new_data.append(id)
            second_id = input("enter the student Second_ID:\n")
            new_data.append(second_id)
            first_name = input("enter the student First Name:\n")
            new_data.append(first_name)
            last_name = input("enter the student Last Name:\n")
            new_data.append(last_name)
            computer_networks = input("enter a mark for Computer Networks:\n")
            new_data.append(computer_networks)
            signals_and_systems = float(input("enter a mark for Signals and Systems:\n"))
            new_data.append(signals_and_systems)
            databases = float(input("enter a mark for Databases:\n"))
            new_data.append(databases)
            calculus = float(input("enter a mark for Calculus:\n"))
            new_data.append(calculus)
            ops = float(input("enter a mark for Operating_Systems:\n"))
            new_data.append(ops)
            ClientSocket.send(command.encode())
            new_data = pickle.dumps(new_data)
            ClientSocket.send(new_data)
            massage = ClientSocket.recv(BUFFER_SIZE).decode()
            print(massage)
            input("press Enter to go back to main menu")
            os.system('clear')
            continue

        elif command == 'Done':
            ClientSocket.send(command.encode())
            ClientSocket.close()
            sys.exit()


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
