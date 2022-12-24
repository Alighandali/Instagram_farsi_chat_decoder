import json

def read_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def write_json(data, output_path):
    with open(output_path, 'w') as res:
            json.dump(data, res, ensure_ascii=False, indent=4)

def read_file(file_path):
    with open(file_path) as f:
        return f.read(f)
