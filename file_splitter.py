import os

def split_file(filepath, chunk_maxsize=1048576) -> int:
    part_num = 0
    with open(filepath, 'rb') as file:
        while True:
            chunk = file.read(chunk_maxsize)
            if not chunk:
                break
            with open(f"{filepath}.part{part_num}", 'wb') as chunk_file:
                chunk_file.write(chunk)
            part_num += 1
    return part_num

def merge_file(filepath, part_num) -> bool:
    with open(filepath, 'wb') as output_file:
        for i in range(part_num):
            part_filepath = f"{filepath}.part{i}"
            if not os.path.exists(part_filepath):
                return False
            with open(part_filepath, 'rb') as part_file:
                output_file.write(part_file.read())
    return True
