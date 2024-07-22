import socket
import os
import file_splitter

def send(send_socket: socket.socket, filepath: str, BUFFER_SIZE: int = 1048576) -> bool:
    try:
        # Split the file into chunks
        print(f"Splitting file: {filepath}")
        part_num = file_splitter.split_file(filepath, BUFFER_SIZE)
        print(f"File split into {part_num} parts.")

        # Send the number of parts
        send_socket.send(str(part_num).encode())
        ack = send_socket.recv(1024).decode()
        if ack != "ACK":
            print("Error: Acknowledgment not received for part number.")
            return False

        # Send each part
        for i in range(part_num):
            part_filepath = f"{filepath}.part{i}"
            print(f"Sending part {i}: {part_filepath}")
            part_size = os.path.getsize(part_filepath)
            send_socket.send(str(part_size).encode())
            ack = send_socket.recv(1024).decode()
            if ack != "ACK":
                print(f"Error: Acknowledgment not received for part size {i}.")
                return False

            with open(part_filepath, 'rb') as part_file:
                while True:
                    data = part_file.read(BUFFER_SIZE)
                    if not data:
                        break
                    send_socket.sendall(data)
            # Wait for the acknowledgment for each part
            ack = send_socket.recv(1024).decode()
            if ack != "ACK":
                print(f"Error: Acknowledgment not received for part {i}.")
                return False

        return True
    except Exception as e:
        print(f"Error during send: {e}")
        return False


def receive(receive_socket: socket.socket, filepath: str) -> bool:
    try:
        # Receive the number of parts
        part_num = int(receive_socket.recv(1024).decode())
        print(f"Receiving {part_num} parts.")
        receive_socket.send("ACK".encode())

        # Receive each part and write to file
        for i in range(part_num):
            part_filepath = f"{filepath}.part{i}"
            print(f"Receiving part {i}: {part_filepath}")
            part_size = int(receive_socket.recv(1024).decode())
            receive_socket.send("ACK".encode())

            received_size = 0
            with open(part_filepath, 'wb') as part_file:
                while received_size < part_size:
                    data = receive_socket.recv(min(1048576, part_size - received_size))
                    if not data:
                        break
                    part_file.write(data)
                    received_size += len(data)
            # Send acknowledgment for each part
            receive_socket.send("ACK".encode())

        # Merge the parts into the final file
        print(f"Merging {part_num} parts into {filepath}")
        if not file_splitter.merge_file(filepath, part_num):
            print("Error: Merging file parts failed.")
            return False

        return True
    except Exception as e:
        print(f"Error during receive: {e}")
        return False
