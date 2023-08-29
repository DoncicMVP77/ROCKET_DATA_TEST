import re

from bs4 import BeautifulSoup


def extract_json_information_from_response_string(cities_information_response_string: str):

    html = BeautifulSoup(cities_information_response_string, 'html.parser')

    json_information = html.find(
        'script',
        string=re.compile(r'window\.initialState')
    ).string

    json_text = re.search(
        r'^\s*window\.initialState\s*=\s*({.*?})\s*\s*$',
        json_information,
        flags=re.DOTALL | re.MULTILINE
    ).group(1)

    return json_text

