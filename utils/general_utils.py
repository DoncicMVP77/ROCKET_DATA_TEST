import json
import os

from requests import Response


def is_json_content(response: Response):
    type_response = response.headers['content-type']

    if 'json' in type_response:
        return True

    return False


def convert_dict_to_json(dict_object: dict) -> json:

    json_object = json.dumps(dict_object, default=str, ensure_ascii=False)

    return json_object


def convert_json_to_dict(json_object: json) -> dict:

    dict_object = json.loads(json_object)

    return dict_object


def write_to_json_file(
        file_path: str,
        json_object: json
) -> None:
    with open(
        os.path.join(
            os.path.dirname(__file__),
            file_path
        ),
        mode='w+',
        encoding='utf-8'
    ) as infile:
        infile.write(json_object)


if __name__ == '__main__':
    write_to_json_file(
        'stzzzzzzatc'
    )