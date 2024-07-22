import socket
import os
import file_splitter

def send(send_socket: socket.socket, filepath: str, BUFFER_SIZE: int = 1048576) -> bool:
    try:
        #split file into chunks
        part_num = file_splitter.split_file(filepath,BUFFER_SIZE)

        #send
        send_socket.send(str(part_num).endcode())

        ack = send_socket.recv(1024).decode()
        if (ack != "ACK"):
            print("Err")
            return False
    
        for i in range(part_num):
            part_filepath = f"{filepath}.part{i}"
            with open(part_filepath, 'rb') as part_file:
                while True:
                    data = part_file.read(BUFFER_SIZE)
                    if not data:
                        break
                    send_socket.send(data)
            ack = send_socket.recv(1024).decode()
            if (ack != "ACK"):
                print("Error")
                return False
                
        return True
    except Exception as e:
        print(f'Error during sending')
        return False
    

def receive(receive_socket: socket.socket, filepath: str) -> bool:
    try:
        part_num = int(receive_socket.recv(1024).decode())

        receive_socket.send("ACK".endcode())

        for i in range (part_num):
            part_filepath = f"{filepath}.part{i}"
            with open(part_filepath, 'wb') as part_file:
                while True:
                    data = receive_socket.rec(1048576)
                    if not data:
                        break
                    part_file.write(data)
            receive_socket.send("ACK".encode())
        if not file_splitter.merge_file(filepath,part_num):
            print("Merge failed")
            return False

        return True
    except Exception as e:
        print(f"Error during reciving: {e}")
        return False
