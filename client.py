import socket
import file_transfer

class Client:
    def __init__(self, SERVER_IP = 'localhost', SERVER_PORT = 9999, BUFFER_SIZE : int = 1048576) -> None:
        # print(f'Client.__init__ @\tCALL @\tFunction called.')
        Client.SERVER_IP = SERVER_IP
        Client.SERVER_PORT = SERVER_PORT
        # Client.SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
        Client.BUFFER_SIZE = BUFFER_SIZE
        Client.MSG_SIZE = 1024

        Client.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            Client.client_socket.connect((SERVER_IP, SERVER_PORT))
        except:
            print(f'Client.__init__ @\tERR @\tConnection Error.')
            Client.CONNECTED = False
        else:
            print(f'Client.__init__ @\tOK @\tConnected to server at {SERVER_IP}:{SERVER_PORT}.')
            Client.CONNECTED = True
    def upload(filepath : str) -> bool:
        # print(f'Client.upload @\tCALL @\tFunction called.')
        Client.client_socket.send(f'REQ@SND@{filepath}'.encode())
        msg = Client.client_socket.recv(Client.MSG_SIZE).decode().strip().split('@')
        if (msg[0] == 'OK' and msg[1] == 'SND'):
            print(f"Client.upload @\tOK @\tFile sending...")
            stat = file_transfer.send(Client.client_socket, filepath, Client.BUFFER_SIZE)
            if (stat):
                print(f"Client.upload @\tOK @\tFile sent.")
                return True
            else:
                print(f"Client.upload @\tERR @\tFile corrupted or not found.")
                return False
        elif (msg[0] == 'ERR' and msg[1] == 'SND'):
            print(f"Client.upload @\tERR @\tRequest denied. {msg[2]}")
            return False
        else:
            print(f"Client.upload @\tERR @\tUnexpected error!")
            return False
    def download(filepath : str) -> bool:
        print(f'Client.download @\tCALL @\tFunction called.')
        Client.client_socket.send(f'REQ@DWN@{filepath}'.encode())
        msg = Client.client_socket.recv(Client.MSG_SIZE).decode().strip().split('@')
        if (msg[0] == 'OK' and msg[1] == 'DWN'):
            print(f"Client.download @\tOK @\tFile downloading...")
            stat = file_transfer.receive(Client.client_socket, filepath)
            if (stat):
                print(f"Client.download @\tOK @\tFile downloaded.")
                return True
            else:
                print(f"Client.download @\tERR @\tFile corrupted or not found.")
                return False
        elif (msg[0] == 'ERR' and msg[1] == 'DWN'):
            print(f"Client.download @\tERR @\tRequest denied. {msg[2]}")
            return False
        else:
            print(f"Client.download @\tERR @\tUnexpected error!")
            return False
    def delete(filepath : str) -> bool:
        # print(f'Client.delete @\tCALL @\tFunction called.')
        Client.client_socket.send(f'REQ@DEL@{filepath}'.encode())
        msg = Client.client_socket.recv(Client.MSG_SIZE).decode().strip().split('@')
        if (msg[0] == 'OK' and msg[1] == 'DEL'):
            print(f'Client.delete @\tOK @\t{msg[2]}')
            return True
        elif (msg[0] == 'ERR' and msg[1] == 'DEL'):
            print(f'Client.delete @\tERR @\t{msg[2]}')
            return False
        else:
            print(f'Client.delete @\tERR @Unexpected error! Msg = {msg}')
            return False
    
    # For GUI
    def setServerAddress(address : str) -> None:
        Client.SERVER_IP, Client.SERVER_PORT = str.split(':')
    def setServerAddress(SERVER_IP : str, SERVER_PORT : int) -> None:
        Client.SERVER_IP = SERVER_IP
        Client.SERVER_PORT = SERVER_PORT

    # For debug purpose
    def main_func(self) -> None:
        while True:
            stat, msg = Client.client_socket.recv(Client.MSG_SIZE).decode().split("@")
            print(msg)
            if (stat == "DISCONNECTED"):
                break

            cmd = input("- DOWNLOAD\n- UPLOAD\n- DELETE\n- EXIT\nChoose:")
            cmd = cmd.split()[0].upper()
            if (cmd == 'EXIT'):
                Client.client_socket.send(f"REQ@LOGOUT@LOGOUT".encode())
                break

            filepath = input("Enter filepath: ")

            if (cmd == 'UPLOAD'):
                if (Client.upload(filepath)):
                    print(f"Uploaded \'{filepath}\' successfully") 
                else:
                    print(f"Cannot upload \'{filepath}\'. Please check if file exist.")
            elif (cmd == 'DOWNLOAD'):
                if (Client.download(filepath)):
                    print(f"Downloaded \'{filepath}\' successfully") 
                else:
                    print(f"Cannot download \'{filepath}\'. Please check if file exist.")
            elif (cmd == 'DELETE'):
                if (Client.delete(filepath)):
                    print(f"Deleted \'{filepath}\' successfully") 
                else:
                    print(f"Cannot delete \'{filepath}\'. Please check if file exist.")
        print("Disconnected from the server.")
        Client.client_socket.close()

if (__name__ == "__main__"):
    IP = input("Enter server IP: ")
    PORT = int(input("Enter server port: "))
    client = Client(IP, PORT)

    while (not client.CONNECTED):
        IP = input("Enter server IP: ")
        PORT = int(input("Enter server port: "))
        client = Client(IP, PORT)

    client.main_func()