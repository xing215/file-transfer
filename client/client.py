import socket
import file_transfer

class Client:
    def __init__(self, SERVER_IP='localhost', SERVER_PORT=9999, BUFFER_SIZE: int = 100048576) -> None:
        # print(f'Client.__init__ @\tCALL @\tFunction called.')
        self.SERVER_IP = SERVER_IP
        self.SERVER_PORT = SERVER_PORT
        # self.SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
        self.BUFFER_SIZE = BUFFER_SIZE
        self.MSG_SIZE = 1024
        self.DEFAULT_PATH = "client_data/"

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
        except:
            print(f'Client.__init__ @\tERR @\tConnection Error.')
            self.CONNECTED = False
        else:
            print(f'Client.__init__ @\tOK @\tConnected to server at {SERVER_IP}:{SERVER_PORT}.')
            self.CONNECTED = True
        
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.CONNECTED = True
        except Exception as e:
            print(f"Connection error: {e}")
            self.CONNECTED = False

    def is_connected(self):
        return self.CONNECTED

    def upload(self, filepath: str) -> bool:
        # print(f'Client.upload @\tCALL @\tFunction called.')
        self.client_socket.send(f'REQ@SND@{filepath}'.encode())
        # if (not '/' in filepath or not '\\' in filepath):
        #     filepath = self.DEFAULT_PATH + filepath
        msg = self.client_socket.recv(self.MSG_SIZE).decode().strip().split('@')    
        if (msg[0] == 'OK' and msg[1] == 'SND'):
            print(f"Client.upload @\tOK @\tFile sending...")
            stat = file_transfer.send(self.client_socket, filepath, self.BUFFER_SIZE)
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
            print(f"Client.upload @\tERR @\tUnexpected error! {msg}")
            return False

    def download(self, filename: str, save_path: str) -> bool:
        print(f'Client.download @\tCALL @\tFunction called.')
        self.client_socket.send(f'REQ@DWN@{filename}'.encode())
        msg = self.client_socket.recv(self.MSG_SIZE).decode().strip().split('@')
        if (msg[0] == 'OK' and msg[1] == 'DWN'):
            print(f"Client.download @\tOK @\tFile downloading...")
            stat = file_transfer.receive(self.client_socket, save_path)
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


    def delete(self, filepath: str) -> bool:
        # print(f'Client.delete @\tCALL @\tFunction called.')
        self.client_socket.send(f'REQ@DEL@{filepath}'.encode())
        msg = self.client_socket.recv(self.MSG_SIZE).decode().strip().split('@')
        if (msg[0] == 'OK' and msg[1] == 'DEL'):
            print(f'Client.delete @\tOK @\t{msg[2]}')
            return True
        elif (msg[0] == 'ERR' and msg[1] == 'DEL'):
            print(f'Client.delete @\tERR @\t{msg[2]}')
            return False
        else:
            print(f'Client.delete @\tERR @Unexpected error! Msg = {msg}')
            return False

    def rename(self, oldname: str, newname: str) -> bool:
        self.client_socket.send(f'REQ@REN@{oldname}@{newname}'.encode())
        msg = self.client_socket.recv(self.MSG_SIZE).decode().strip().split("@")
        if (msg[0] == 'OK' and msg[1] == 'REN'):
            print(f'Client.rename @\tOK @\t{msg[2]}')
            return True
        elif (msg[0] == 'ERR' and msg[1] == 'REN'):
            print(f'Client.rename @\tERR @\t{msg[2]}')
        else:
            print(f'Client.rename @\tERR @Unexpected error! Msg = {msg}')
            return False
    
    def list_files(self):
        try:
            self.client_socket.sendall("LIST".encode())
            data = self.client_socket.recv(self.MSG_SIZE).decode()
            if data.startswith("LIST@"):
                file_list = data[5:]  # Extract the file list after 'LIST@'
                if file_list == "No files found.":
                    print(file_list)
                    return []
                else:
                    print(f"Files received: {file_list}")
                    return file_list.split("\n")
            else:
                print("Unexpected response from the server.")
                return []
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    # For GUI
    def setServerAddress(address: str) -> None:
        ip, port = str.split(':')
        Client.setServerAddress(ip, int(port))

    def setServerAddress(SERVER_IP: str, SERVER_PORT: int) -> None:
        Client.SERVER_IP = SERVER_IP
        Client.SERVER_PORT = SERVER_PORT

    # For debug purpose
    def main_func(self) -> None:
        while True:
            stat, msg = self.client_socket.recv(self.MSG_SIZE).decode().split("@")
            print(msg)
            if (stat == "DISCONNECTED"):
                break

            cmd = input("- DOWNLOAD\n- UPLOAD\n- DELETE\n- EXIT\nChoose:")
            cmd = cmd.split()[0].upper()
            if (cmd == 'EXIT'):
                self.client_socket.send(f"REQ@LOGOUT@LOGOUT".encode())
                break

            filepath = input("Enter filepath: ")

            if (cmd == 'UPLOAD'):
                if (self.upload(filepath)):
                    print(f"Uploaded \'{filepath}\' successfully")
                else:
                    print(f"Cannot upload \'{filepath}\'. Please check if file exist.")
            elif (cmd == 'DOWNLOAD'):
                if (self.download(filepath)):
                    print(f"Downloaded \'{filepath}\' successfully")
                else:
                    print(f"Cannot download \'{filepath}\'. Please check if file exist.")
            elif (cmd == 'DELETE'):
                if (self.delete(filepath)):
                    print(f"Deleted \'{filepath}\' successfully")
                else:
                    print(f"Cannot delete \'{filepath}\'. Please check if file exist.")
            elif (cmd == "RENAME"):
                oldname, newname = filepath.strip().split('@')
                if (self.rename(oldname, newname)):
                    print(f"Renamed \'{oldname}\' to \'{newname}\'.")
                else:
                    print(f"Cannot rename \'{oldname}\'. Please check if file exist.")

        print("Disconnected from the server.")
        self.client_socket.close()

if __name__ == "__main__":
    IP = input("Enter server IP: ")
    PORT = int(input("Enter server port: "))
    client = Client(IP, PORT)

    while (not client.CONNECTED):
        IP = input("Enter server IP: ")
        PORT = int(input("Enter server port: "))
        client = Client(IP, PORT)

    client.main_func()