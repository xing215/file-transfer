import socket
import threading
from file_splitter import split_file, merge_file

def download_part(part_filepath: str, receive_socket: socket.socket, buffer_size: int):
    with open(part_filepath, 'wb') as part_file:
        while True:
            data = receive_socket.recv(buffer_size)
            if not data:
                break
            part_file.write(data)

def upload_part(part_filepath: str, send_socket: socket.socket, buffer_size: int):
    with open(part_filepath, 'rb') as part_file:
        while True:
            data = part_file.read(buffer_size)
            if not data:
                break
            send_socket.sendall(data)

def send(filepath: str, send_socket: socket.socket, buffer_size: int) -> bool:
    try:
        # Split file and get number of parts
        part_num = split_file(filepath)
        send_socket.sendall(f"{part_num}".encode())

        def upload_thread(part_filepath: str):
            try:
                upload_part(part_filepath, send_socket, buffer_size)
            except Exception as e:
                print(f"Error uploading part {part_filepath}: {e}")

        threads = []
        for i in range(part_num):
            part_filepath = f"{filepath}.part{i}"
            thread = threading.Thread(target=upload_thread, args=(part_filepath,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()        
        return True
    except Exception as e:
        print(f"Error in sending file: {e}")
        return False


def receive(filepath: str, receive_socket: socket.socket, buffer_size: int) -> bool:
    try:
        # Receive number of parts
        part_num = int(receive_socket.recv(1024).decode())

        def download_thread(part_filepath: str):
            try:
                download_part(part_filepath, receive_socket, buffer_size)
            except Exception as e:
                print(f"Error downloading part {part_filepath}: {e}")

        threads = []
        for i in range(part_num):
            part_filepath = f"{filepath}.part{i}"
            thread = threading.Thread(target=download_thread, args=(part_filepath,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        return merge_file(filepath, part_num)
    except Exception as e:
        print(f"Error in receiving file: {e}")
        return False
