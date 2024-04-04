import json
import os

def save(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"{filename} created")

def load_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text