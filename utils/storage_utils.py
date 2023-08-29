import json
from pathlib import Path


def save_json(json_object: json, path_object: Path):

    with open(path_object, encoding='utf-8', mode='w+') as infile:
        infile.write(json_object)