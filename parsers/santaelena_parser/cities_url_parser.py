import json
import re

from requests import Session
from bs4 import BeautifulSoup

from config import SANTA_ELENA_BASE_HEADERS, SANTA_ELENA_CITIES_URL
from utils.requests_utils import fetch_data, init_browser_session, close_browser_session


def get_cities_url_list(browser_session: Session) -> list[str]:

    cities_information_response_string = get_cafes_cities_information_response_string(
        cities_information_url=SANTA_ELENA_CITIES_URL,
        browser_session=browser_session
    )

    list_city_urls = fetch_cities_information_list(cities_information_response_string)

    return list_city_urls


def fetch_cities_information_list(cities_information_response_string: str):

    html = BeautifulSoup(cities_information_response_string, 'html.parser')

    list_city = html.find_all('ul', class_='sub-menu elementor-nav-menu--dropdown')[1].find_all('li')

    list_city_url = [city.find('a').get('href') for city in list_city]

    return list_city_url


def get_cafes_cities_information_response_string(
        cities_information_url: str,
        browser_session: Session
) -> str:
    hospital_cities_response = fetch_data(
        url=cities_information_url,
        browser_session=browser_session
    )

    return hospital_cities_response


if __name__ == '__main__':

    browser_session = init_browser_session(headers=SANTA_ELENA_BASE_HEADERS)

    list_cities_url = get_cities_url_list(browser_session)

    print(list_cities_url)

    close_browser_session(browser_session)

