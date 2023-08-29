import re

from requests import Session
from bs4 import BeautifulSoup

from decorators.format_information_decorator import format_phone_numbers_decorator, \
    format_dentalia_hospital_name_decorator, format_hospital_latlon_decorator, format_hospital_working_hours_decorator
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


def get_list_hospital_information(
        list_hospitals_id_and_latlon: list[dict],
        browser_session: Session
) -> dict:

    hospitals_information_list = []

    for hospital_dict in list_hospitals_id_and_latlon:

        hospital_cities_response_text = get_hospital_information_response_by_hospital_id(
            hospital_id=hospital_dict['hospital_id'],
            browser_session=browser_session
        )

        dict_hospital_information = fetch_hospital_information(
            hospital_information_response_text=hospital_cities_response_text,
            hospital_dict=hospital_dict
        )


        # formatter_dict = format_hospital_information_dict(
        #     hospital_information_dict=dict_hospital_information
        # )

        hospitals_information_list.append(dict_hospital_information)

    hospitals_information_dict = {
        'hospitals': hospitals_information_list
    }

    return hospitals_information_dict


def fetch_hospital_information(
        hospital_information_response_text: str,
        hospital_dict: dict
):

    html = BeautifulSoup(hospital_information_response_text, 'html.parser')

    string_hospital_name = _get_hospital_name(html=html)

    string_hospital_address = _get_hospital_address(html=html)

    list_hospital_phones = _get_hospital_phone_numbers(html=html)

    string_hospital_working_hours = _get_hospital_working_hours(html=html)

    list_hospital_latlon = _get_hospital_latlon(hospital_dict=hospital_dict)

    dict_hospital_information =generate_hospital_information_dict(
        string_hospital_name=string_hospital_name,
        string_hospital_address=string_hospital_address,
        list_hospital_phone_numbers=list_hospital_phones,
        list_string_working_hours=string_hospital_working_hours,
        list_string_latlon=list_hospital_latlon
    )

    return dict_hospital_information


def generate_hospital_information_dict(
    string_hospital_name: str,
    string_hospital_address: str,
    list_hospital_phone_numbers: list[str],
    list_string_working_hours: list[str],
    list_string_latlon: list[float, float]
) -> dict:

    dict_hospital_information = {
        'name': string_hospital_name,
        'address': string_hospital_address,
        'phones': list_hospital_phone_numbers,
        'working_hours': list_string_working_hours,
        'latlon': list_string_latlon
    }

    return dict_hospital_information

def _get_hospital_name(html: BeautifulSoup) -> str:
    string_hospital_name = _fetch_hospital_name(html=html)

    formatted_hospital_name = _format_hospital_name(
        string_hospital_name=string_hospital_name
    )

    return formatted_hospital_name


def _fetch_hospital_name(html: BeautifulSoup) -> str:

    try:
        hospital_name = str(html.find('h3', class_='elementor-heading-title elementor-size-default').text)
    except AttributeError as e:
        hospital_name = ''
    else:
        return hospital_name


def _format_hospital_name(string_hospital_name: str) -> str:
    formatted_hospital_name = 'dentalia ' + string_hospital_name

    return formatted_hospital_name


def _get_hospital_address(html: BeautifulSoup) -> str:

    string_hospital_address = _fetch_hospital_address(html=html)

    formatted_string_hospital_address = _format_hospital_address(
        string_hospital_address=string_hospital_address
    )

    return formatted_string_hospital_address


def _fetch_hospital_address(html: BeautifulSoup) -> str:

    try:
        hospital_address = str(
            html.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[0].
            find('div', class_='jet-listing-dynamic-field__content').text
        )
    except AttributeError as e:
        hospital_address = ''
    else:
        return hospital_address


def _format_hospital_address(string_hospital_address: str) -> str:
    return string_hospital_address.strip('.')


def _get_hospital_latlon(hospital_dict: dict) -> list[float, float]:
    dict_hospital_latlon = _fetch_hospital_latlon(hospital_dict=hospital_dict)

    formatted_list_hospital_latlon = _format_hospital_latlon(
        dict_hospital_latlon=dict_hospital_latlon
    )

    return formatted_list_hospital_latlon


def _fetch_hospital_latlon(hospital_dict: dict) -> dict:

    return hospital_dict['latlon']


def _format_hospital_latlon(dict_hospital_latlon: dict) -> list[float, float]:

    formatted_list_hospital_latlon = [
        float(dict_hospital_latlon['lat']),
        float(dict_hospital_latlon['lng'])
    ]

    return formatted_list_hospital_latlon


def _get_hospital_phone_numbers(html: BeautifulSoup) -> list:

    string_hospital_phone_numbers = _fetch_hospital_phone_numbers(html=html)

    formatted_list_phone_numbers = _format_hospital_phone_numbers(
        string_hospital_phone_numbers=string_hospital_phone_numbers
    )

    return formatted_list_phone_numbers


def _fetch_hospital_phone_numbers(html: BeautifulSoup) -> str:

    try:
        hospital_phones = str(
            html.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[2].
            find('div', class_='jet-listing-dynamic-field__content').text
        )
    except AttributeError as e:
        hospital_phones = ''
    else:
        return hospital_phones


def _format_hospital_phone_numbers(string_hospital_phone_numbers: str) -> list[str]:
    list_hospital_phone_numbers = string_hospital_phone_numbers.strip().strip('.').split('\r')

    formatted_list_phone_numbers = [
        "".join(hospital_phone_number.strip().split())
        for hospital_phone_number in list_hospital_phone_numbers
    ]

    return formatted_list_phone_numbers


def _get_hospital_working_hours(html: BeautifulSoup) -> list[str]:

    string_hospital_working_hours = _fetch_working_hours(html=html)

    formatted_list_hospital_working_hours = _format_hospital_working_hours(
        string_hospital_working_hours=string_hospital_working_hours
    )

    return formatted_list_hospital_working_hours


def _fetch_working_hours(html: BeautifulSoup) -> str:

    try:
        string_hospital_working_hours = str(
            html.find_all('div', class_='jet-listing jet-listing-dynamic-field display-inline')[1].
            find('div', class_='jet-listing-dynamic-field__content').text
        ).strip()

    except AttributeError as e:
        hospital_working_hours_string = ''
    else:
        return string_hospital_working_hours


def _format_hospital_working_hours(string_hospital_working_hours: str) -> list[str]:

    formatted_string_hospital_working_hours = re.sub(
        "^\s+|\n|\s+$",
        " ",
        re.sub("^\s+|\r|\s+$", "", string_hospital_working_hours)
    ).strip()

    return [formatted_string_hospital_working_hours]


def get_hospital_information_response_by_hospital_id(
        hospital_id: str,
        browser_session: Session
) -> str:

    params['post_id'] = hospital_id

    hospital_cities_response = fetch_data(
        url=hospital_detail_url,
        browser_session=browser_session,
        params=params
    )

    return hospital_cities_response['html']


if __name__ == '__main__':

    browser_session = init_session(headers=headers)

    hospital_information_list = get_list_hospital_information(browser_session=browser_session, list_hospitals_id_and_latlon=[{
            "hospital_id": 1353,
            "latlon": {
                "lat": "21.9245323",
                "lng": "-102.2897871"
            }
        }])

    print(hospital_information_list)

    close_session(browser_session=browser_session)
