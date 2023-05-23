import os

def list_to_file(data, path):
    with open(path, 'w') as f:
        for line in data:
            f.write(f"{line}\n")