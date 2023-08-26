import re

from requests import Session
from bs4 import BeautifulSoup

from decorators.format_information_decorator import format_phone_numbers_decorator, \
    format_dentalia_hospital_name_decorator
from utils.requests_utils import fetch_data, init_session, close_session

params = {
    'listing_id': '6640',
    'post_id': '1355',
    'source': 'posts',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'PHPSESSID=80i9pdv7hv7rbqmau7678t8lmf; _lscache_vary=7f9211ff83e640e486010157d7d75cd1',
    'Origin': 'https://dentalia.com',
    'Referer': 'https://dentalia.com/clinica/?jsf=jet-engine:clinicas-archive&tax=estados:26',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

hospital_detail_url = 'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/'


def get_list_hospital_information(list_hospitals_id_and_latlon: list[dict], session: Session):
    hospitals_information_list = []

    for hospital_dict in list_hospitals_id_and_latlon:

        hospital_cities_response_text = get_hospital_information_response_by_hospital_id(
            hospital_id=hospital_dict['hospital_id'],
            session=session
        )

        dict_hospital_information = fetch_hospital_information(
            hospital_information_response_text=hospital_cities_response_text
        )

        # formatter_dict = format_hospital_information_dict(
        #     hospital_information_dict=dict_hospital_information
        # )

        hospitals_information_list.append(dict_hospital_information)

    return hospitals_information_list


def fetch_hospital_information(
        hospital_information_response_text: str,
        hospital_dict: dict
):

    html = BeautifulSoup(hospital_information_response_text, 'html.parser')

    hospital_name = fetch_hospital_name(html=html)

    hospital_address = fetch_hospital_address(html=html)

    hospital_phones = fetch_hospital_phones(html=html)

    string_hospital_working_hours = fetch_working_hours(html=html)

    dict_hospital_information = {
        'name': hospital_name,
        'address': hospital_address,
        'phones': hospital_phones,
        'working_hours': string_hospital_working_hours
    }

    print(dict_hospital_information)

    return dict_hospital_information


@format_dentalia_hospital_name_decorator
def fetch_hospital_name(html: BeautifulSoup) -> str:

    try:
        hospital_name = str(html.find('h3', class_='elementor-heading-title elementor-size-default').text)
    except Exception as e:
        hospital_name = ''
    else:
        return hospital_name


def fetch_hospital_address(html: BeautifulSoup) -> str:

    try:
        hospital_address = str(
            html.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[0].
            find('div', class_='jet-listing-dynamic-field__content').text
        ).strip('.')
    except Exception:
        hospital_address = ''
    else:
        return hospital_address


def fetch_hospital_latlon(html: BeautifulSoup) -> list[float, float]:
    pass


@format_phone_numbers_decorator
def fetch_hospital_phones(html: BeautifulSoup) -> str:

    try:
        hospital_phones = str(
            html.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[2].
            find('div', class_='jet-listing-dynamic-field__content').text
        ).strip()
    except Exception:
        hospital_phones = ''
    else:
        return hospital_phones


def fetch_working_hours(html: BeautifulSoup) -> str:

    try:
        hospital_working_hours_string = str(
            html.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[1].
            find('div', class_='jet-listing-dynamic-field__content').text
        ).strip()
    except Exception:
        hospital_working_hours_string = ''
    else:
        return hospital_working_hours_string


def format_hospital_information_dict(hospital_information_dict: dict):

    phone_numbers = format_hospital_phone_numbers(
        hospital_phone_numbers_string=hospital_information_dict['phones']
    )


def

def format_hospital_phone_numbers(hospital_phone_numbers_string: str):

    list_hospital_phone_numbers = hospital_phone_numbers_string.split('\r')

    list_formatter_phone_numbers = [
        "".join(hospital_phone_number.strip().split())
        for hospital_phone_number in list_hospital_phone_numbers
    ]

    print(list_formatter_phone_numbers)

    return list_hospital_phone_numbers



def get_hospital_information_response_by_hospital_id(hospital_id: str, session: Session):
    params['post_id'] = hospital_id

    hospital_cities_response = fetch_data(
        url=hospital_detail_url,
        session=session,
        params=params
    )

    print(hospital_cities_response)

    return hospital_cities_response['html']


if __name__ == '__main__':

    session = init_session(headers=headers)

    hospital_information_list = get_list_hospital_information(session=session, list_hospitals_id_and_latlon=['1327'])

    print(hospital_information_list)

    close_session(session=session)
