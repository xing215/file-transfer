import os
import socket
import threading

lock = threading.Lock()

def send_chunk(send_socket: socket.socket, chunk: bytes):
    try:
        with lock:
            send_socket.sendall(chunk)
    except Exception as e:
        print(f"send_chunk @\tERR @\t{e}")

def send(send_socket: socket.socket, filepath: str, chunk_size: int = 1048576) -> bool:
    try:
        file_size = os.path.getsize(filepath)
        num_chunks_List = file_size // chunk_size + (1 if file_size % chunk_size != 0 else 0)

        send_socket.send(str(num_chunks_List).encode())
        ACK = send_socket.recv(chunk_size).decode()
        if ACK != f"OK@{num_chunks_List}"
            raise "ACK ERR"
        with open(filepath, 'rb') as f:
            threads = []
            for i in range(num_chunks_List):
                chunk = f.read(chunk_size)
                thread = threading.Thread(target=send_chunk, args=(send_socket, chunk))
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()
        
        return True
    except Exception as e:
        print(f"send @\tERR @\t{e}")
        return False

def receive_chunk(receive_socket: socket.socket, chunk_size: int, chunks_List: list):
    try:
        chunks_List.append(receive_socket.recv(chunk_size))
    except Exception as e:
        print(f"receive_chunk @\tERR @\t{e}")

def receive(receive_socket: socket.socket, filepath: str, chunk_size: int = 1048576) -> bool:
    try:
        num_chunks_List = int(receive_socket.recv(chunk_size).decode())
        receive_socket.send(f"OK@{num_chunks_List}".encode())
        chunks_List = []
        threads = []
        
        for i in range(num_chunks_List):
            thread = threading.Thread(target=receive_chunk, args=(receive_socket, chunk_size, chunks_List))
            thread.start()
            threads.append(thread)
        for thr in threads:
            thr.join()
        with open(filepath, 'wb') as file:
            for part in chunks_List:
                if part:
                    file.flush()
                    file.write(part)
        return True
    except Exception as e:
        print(f"receive @\tERR @\t{e}")
        return False