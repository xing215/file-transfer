import os
import socket
import threading

def send_chunk(send_socket: socket.socket, chunk: bytes):
    try:
        send_socket.sendall(chunk)
    except Exception as e:
        print(f"send_chunk @\tERR @\t{e}")

def send(send_socket: socket.socket, filepath: str, chunk_size: int = 1048576) -> bool:
    try:
        file_size = os.path.getsize(filepath)
        num_chunks_List = file_size // chunk_size + (1 if file_size % chunk_size != 0 else 0)

        with open(filepath, 'rb') as f:
            threads = []
            for i in range(num_chunks_List):
                chunk = f.read(chunk_size)
                thread = threading.Thread(target=send_chunk, args=(send_socket, chunk))
                thread.start()
                threads.append(thread)
            
            for thread in threads:
                thread.join()

        send_chunk(send_socket, b'EOF')  

        return True
    except Exception as e:
        print(f"send @\tERR @\t{e}")
        return False

def receive_chunk(receive_socket: socket.socket, chunk_size: int, chunks_List: list, index: int):
    try:
        chunks_List[index] = receive_socket.recv(chunk_size)
    except Exception as e:
        print(f"receive_chunk @\tERR @\t{e}")

def receive(receive_socket: socket.socket, filepath: str, chunk_size: int = 1048576) -> bool:
    try:
        chunks_List = []
        index = 0
        while True:
            chunks_List.append(None)
            thread = threading.Thread(target=receive_chunk, args=(receive_socket, chunk_size, chunks_List, index))
            thread.start()
            thread.join()  # Cái này cần fix, tại này đang nhận được data nào là gộp vô luôn
            if chunks_List[index] == b'EOF':
                chunks_List.pop()  
                break
            index += 1

        with open(filepath, 'wb') as file:
            for part in chunks_List:
                if part:
                    file.write(part)
                    file.flush()
        return True
    except Exception as e:
        print(f"receive @\tERR @\t{e}")
        return False