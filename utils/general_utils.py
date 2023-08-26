from requests import Response


def is_json_content(response: Response):
    type_response = response.headers['content-type']

    if 'json' in type_response:
        return True

    return False
