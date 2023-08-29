import json
import re

from bs4 import BeautifulSoup
from requests import Session

from config import YAPDOMIK_BASE_HEADERS, YAPDOMIK_CITIES_URL, YAPDOMIK_CITIES_URL_FORMAT
from utils.requests_utils import fetch_data, init_session, close_session


def get_cities_url_list(browser_session: Session) -> list[str]:

    cities_information_response_string = _get_cafes_cities_information_response_string(
        cities_information_url=YAPDOMIK_CITIES_URL,
        browser_session=browser_session
    )

    dict_information = _extract_json_information_from_response_string(
        cities_information_response_string=cities_information_response_string
    )

    list_city_information = _fetch_cities_information_list(dict_information)

    list_city_url = _generate_cities_url_list(list_city_information)

    return list_city_url


def _generate_cities_url_list(list_city_information: dict):

    list_city_url = [
        YAPDOMIK_CITIES_URL_FORMAT.format(city_alias=city_information['translitAlias'])
        for city_information in list_city_information
    ]

    return list_city_url


def _fetch_cities_information_list(dict_information: dict):

    try:
        list_city = dict_information['cityList']
    except KeyError as e:
        print(e)
    else:
        return list_city


def _extract_json_information_from_response_string(cities_information_response_string: str):

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


def _get_cafes_cities_information_response_string(
        cities_information_url: str,
        browser_session: Session
) -> str:

    hospital_cities_response = fetch_data(
        url=cities_information_url,
        browser_session=browser_session
    )

    return hospital_cities_response


if __name__ == '__main__':

    browser_session = init_session(headers=YAPDOMIK_BASE_HEADERS)

    list_cities_url = get_cities_url_list(browser_session)

    print(list_cities_url)

    close_session(browser_session)

