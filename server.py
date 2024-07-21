import os
import socket
import threading
import file_transfer

class Server:
    def __init__(self, SERVER_PORT : int = 9999,BUFFER_SIZE : int = 1048576) -> None:
        Server.BUFFER_SIZE = BUFFER_SIZE
        Server.IP = socket.gethostbyname(socket.gethostname())
        Server.PORT = SERVER_PORT
        Server.MSG_SIZE = 1024
        Server.DEFAULT_PATH = "server_data/"

        Server.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server.server_socket.bind((Server.IP, Server.PORT))
        Server.server_socket.listen()
        print(f"Server.__init__ @ \tOK @\tServer is listening on {Server.IP}:{Server.PORT}.")
    def upload(conn : socket, filepath : str) -> bool:
        conn.send(f"OK@SND@Waiting for file...".encode())
        if (not '/' in filepath or not '\\' in filepath):
            filepath = Server.DEFAULT_PATH + filepath
        if (file_transfer.receive(conn, filepath)):
            print(f"Server.upload @\tOK @\File received")
            return True
        else:
            print(f"Server.upload @\tERR @\tFile corrupted or not found.")
            return False
    def download(conn : socket, filepath : str) -> bool:
        conn.send(f"OK@DWN@Sending file...".encode())
        if (not '/' in filepath or not '\\' in filepath):
            filepath = Server.DEFAULT_PATH + filepath
        if (file_transfer.send(conn, filepath)):
            print(f"Server.download @\tOK @\File sent")
            return True
        else:
            print(f"Server.download @\tERR @\tFile corrupted or not found.")
            return False

    def delete(conn: socket, filepath : str) -> bool:
        if (not os.path.isfile(filepath)):
            print(f"Server.delete @\tERR @\tFile not found!")
            conn.send(f"ERR@DEL@\"{filepath}\" not found!".encode())
            return False
        
        os.remove(filepath)
        print(f"Server.delete @\tOK @\tFile deleted.")
        conn.send(f"OK@DEL@\"{filepath}\" not found!".encode())
        return True


    def handle_client(conn : socket, addr):
        print(f"Server @\tOK @\t{addr} connected.")
        conn.send(f"OK@\nConnection set.\n".encode())

        while True:
            data, cmd, filepath = conn.recv(Server.BUFFER_SIZE).decode().split('@')
            if (data != 'REQ'):
                continue
            
            if (cmd == 'SND'):
                if (not Server.upload(conn, filepath)):
                    print(f"Function upload return error.")
            elif (cmd == 'DWN'):
                if (not Server.download(conn, filepath)):
                    print(f"Function download return error.")
            elif (cmd == 'DEL'):
                if (not Server.delete(conn, filepath)):
                    print(f"Function delete return error.")
            elif (cmd == 'LOGOUT'):
                break
            
            conn.send(f"OK@\n".encode())
            
        print(f"[DISCONNECTED] {addr} disconnected")
        conn.close()


    def main_func(self) -> None:
        while True:
            conn, addr = Server.server_socket.accept()
            thread = threading.Thread(target=Server.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if (__name__ == "__main__"):
    server = Server()
    server.main_func()