import json
import os


def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        create(file_path)
        return False

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        if not data:
            return {}
        return json.loads(data)

def write_file(file_path, data={}):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def create(file_path):
    open(file_path, 'w').close()


def update(file_path, new_item={}):
    if not ensure_file_exists(file_path):
        write_file(file_path, new_item)
        return
    data = read_file(file_path)
    new_key, new_val = list(new_item.keys()), list(new_item.values())

    for key, val in zip(new_key, new_val):
        if key in data:  # Check if key exists and value matches
            data[key] = new_item[key]  # Update with the new item

    write_file(file_path, data)  # Save the updated data

