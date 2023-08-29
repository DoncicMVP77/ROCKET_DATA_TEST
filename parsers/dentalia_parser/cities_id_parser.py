from bs4 import BeautifulSoup
from requests import Session

from config import DENTALIA_BASE_HEADERS, DENTALIA_HOPSITAL_CITIES_URL
from utils.requests_utils import fetch_data, init_session, close_session


def get_list_cities_id(browser_session: Session):

    hospital_cities_response = _get_cities_response(
        url=DENTALIA_HOPSITAL_CITIES_URL,
        browser_session=browser_session,
    )

    list_cities_id = _fetch_cities_id(
        site_response=hospital_cities_response
    )

    return list_cities_id


def _fetch_cities_id(site_response: str):

    html = BeautifulSoup(site_response, 'html.parser')

    list_cities = html.find('select', class_='jet-select__control').find_all('option')

    list_cities_id = [cities['value'] if cities['value'] != '' else None for cities in list_cities ]

    return list_cities_id


def _get_cities_response(
    url: str,
    browser_session: Session
):

    hospital_cities_response = fetch_data(
        url=url,
        browser_session=browser_session
    )

    return hospital_cities_response


if __name__ == '__main__':

    browser_session = init_session(
        headers=DENTALIA_BASE_HEADERS
    )

    list_cities_id = get_list_cities_id(
        browser_session=browser_session
    )

    print(list_cities_id)

    close_session(
        browser_session=browser_session
    )

