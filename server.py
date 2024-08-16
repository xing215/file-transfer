import os
import socket
import threading
import file_transfer

class Server:
    def __init__(self, SERVER_PORT: int = 9999, BUFFER_SIZE: int = 100048576) -> None:
        self.BUFFER_SIZE = BUFFER_SIZE
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = SERVER_PORT
        self.MSG_SIZE = 1024
        # Lấy đường dẫn tuyệt đối của thư mục chứa tệp server.py
        self.BASE_PATH = os.path.abspath(os.path.dirname(__file__))
        # Đặt DEFAULT_PATH là đường dẫn tuyệt đối tới thư mục server_data/
        self.DEFAULT_PATH = os.path.join(self.BASE_PATH, "server_data/")

        # Tạo thư mục server_data nếu chưa tồn tại
        if not os.path.exists(self.DEFAULT_PATH):
            os.makedirs(self.DEFAULT_PATH)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen()
        print(f"Server.__init__ @ \tOK @\tServer is listening on {self.IP}:{self.PORT}.")

    def upload(self, conn: socket.socket, filepath: str) -> bool:
        conn.send(f"OK@SND@Waiting for file...".encode())
        # Đảm bảo filepath là đường dẫn tuyệt đối
        if not ('/' in filepath or '\\' in filepath):
            filepath = os.path.join(self.DEFAULT_PATH, filepath)
        else:
            # Nếu filepath có chứa đường dẫn, chỉ lấy tên file
            filepath = os.path.join(self.DEFAULT_PATH, os.path.basename(filepath))
        if file_transfer.receive(conn, filepath, self.BUFFER_SIZE):
            print(f"Server.upload @\tOK @\tFile received")
            return True
        else:
            print(f"Server.upload @\tERR @\tFile corrupted or not found.")
            return False

    def download(self, conn: socket.socket, filepath: str) -> bool:
        conn.send(f"OK@DWN@Sending file...".encode())
        # Đảm bảo filepath là đường dẫn tuyệt đối
        if not ('/' in filepath or '\\' in filepath):
            filepath = os.path.join(self.DEFAULT_PATH, filepath)
        else:
            filepath = os.path.join(self.DEFAULT_PATH, os.path.basename(filepath))
        if file_transfer.send(conn, filepath):
            print(f"Server.download @\tOK @\tFile sent")
            return True
        else:
            print(f"Server.download @\tERR @\tFile corrupted or not found.")
            return False

    def delete(self, conn: socket.socket, filepath: str) -> bool:
        if not ('/' in filepath or '\\' in filepath):
            filepath = os.path.join(self.DEFAULT_PATH, filepath)
        else:
            filepath = os.path.join(self.DEFAULT_PATH, os.path.basename(filepath))

        if not os.path.isfile(filepath):
            print(f"Server.delete @\tERR @\tFile not found!")
            conn.send(f"ERR@DEL@\"{filepath}\" not found!".encode())
            return False

        os.remove(filepath)
        print(f"Server.delete @\tOK @\tFile deleted.")
        conn.send(f"OK@DEL@\"{filepath}\" deleted.".encode())
        return True

    def rename(self, conn: socket.socket, filenames: str) -> bool:
        oldname, newname = filenames.strip().split('@')
        if not ('/' in oldname or '\\' in oldname):
            oldname = os.path.join(self.DEFAULT_PATH, oldname)
        else:
            oldname = os.path.join(self.DEFAULT_PATH, os.path.basename(oldname))
        if not ('/' in newname or '\\' in newname):
            newname = os.path.join(self.DEFAULT_PATH, newname)
        else:
            newname = os.path.join(self.DEFAULT_PATH, os.path.basename(newname))
        if not os.path.isfile(oldname):
            conn.send(f"ERR@REN@\"{oldname}\" not found.".encode())
            return False

        os.rename(oldname, newname)
        conn.send(f"OK@REN@\"{oldname}\" renamed to \"{newname}\".".encode())
        print(f"Server.rename @\tOK @\tFile renamed.")
        return True

    def list_files(self, conn: socket.socket):
        # Send the list of files in the server_data/ directory to the client.
        try:
            # Get the list of files in the DEFAULT_PATH directory
            file_list = os.listdir(self.DEFAULT_PATH)
            file_list_str = "\n".join(file_list) if file_list else "No files found."
            
            # Debugging output to ensure correct file list
            print(f"Files in server_data: {file_list}")

            # Send the file list to the client
            conn.send(f"LIST@{file_list_str}".encode())
        except Exception as e:
            print(f"Server.list_files @\tERR @\t{e}")
            conn.send("ERR@LIST@Failed to retrieve file list.".encode())

    def handle_client(self, conn: socket.socket, addr):
        print(f"Server @\tOK @\t{addr} connected.")
        conn.send(f"OK@\nConnection set.\n".encode())

        while True:
            try:
                data = conn.recv(self.MSG_SIZE).decode().strip()
                print(f"Received data: {data}")  # Debugging statement
                if not data:
                    break

                if '@' in data:
                    cmd, argument = data.split('@', 1)
                else:
                    cmd = data
                    argument = None

                if cmd == 'REQ':
                    if argument.startswith('SND'):
                        if not self.upload(conn, argument[4:]):
                            print("Function upload returned an error.")
                    elif argument.startswith('DWN'):
                        if not self.download(conn, argument[4:]):
                            print("Function download returned an error.")
                    elif argument.startswith('DEL'):
                        if not self.delete(conn, argument[4:]):
                            print("Function delete returned an error.")
                    elif argument.startswith('REN'):
                        filenames = argument[4:]  # Extract filenames
                        if not self.rename(conn, filenames):
                            print("Function rename returned an error.")
                    elif argument == 'LOGOUT':
                        break
                    else:
                        conn.send("ERR@CMD@Unknown command.".encode())
                elif cmd == 'LIST':  # New command for listing files
                    self.list_files(conn)
                else:
                    conn.send("ERR@CMD@Invalid request.".encode())
            except Exception as e:
                print(f"Server.handle_client @\tERR @\t{e}")
                break

        print(f"[DISCONNECTED] {addr} disconnected")
        conn.close()


    def main_func(self) -> None:
        while True:
            conn, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    server = Server()
    server.main_func()