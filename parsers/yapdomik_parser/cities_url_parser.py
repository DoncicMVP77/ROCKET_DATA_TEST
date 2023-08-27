import json
import re

from requests import Session
from bs4 import BeautifulSoup

from utils.requests_utils import fetch_data, init_session, close_session

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://omsk.yapdomik.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 '
                  'Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

string_cities_url = 'https://omsk.yapdomik.ru/about'

string_cities_url_format = 'https://{city_alias}.yapdomik.ru/about'


def get_cities_url_list(session: Session) -> list[str]:

    cities_information_response_string = get_shops_cities_information_response_string(
        cities_information_url=string_cities_url,
        session=session
    )

    dict_information = extract_json_information_from_response_string(
        cities_information_response_string=cities_information_response_string
    )

    list_city_information = fetch_cities_information_list(dict_information)

    list_city_url = generate_cities_url_list(list_city_information)

    return list_city_url


def generate_cities_url_list(list_city_information: dict):

    list_city_url = [
        string_cities_url_format.format(city_alias=city_information['translitAlias'])
        for city_information in list_city_information
    ]

    return list_city_url





def fetch_cities_information_list(dict_information: dict):

    try:
        list_city = dict_information['cityList']
    except KeyError as e:
        print(e)
    else:
        return list_city


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

    dict_information = json.loads(json_text)

    return dict_information


def get_shops_cities_information_response_string(cities_information_url: str, session: Session) -> str:
    hospital_cities_response = fetch_data(
        url=cities_information_url,
        session=session
    )

    return hospital_cities_response

if __name__ == '__main__':

    session = init_session(headers=headers)

    list_cities_url = get_cities_url_list(session)

    print(list_cities_url)

    close_session(session)

