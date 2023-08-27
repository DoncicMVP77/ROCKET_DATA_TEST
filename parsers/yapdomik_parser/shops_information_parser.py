from requests import Session

from decorators.format_information_decorator import format_hospital_latlon_decorator
from parsers.yapdomik_parser.cities_url_parser import get_cities_url_list
from parsers.yapdomik_parser.yapdomik_utils import extract_json_information_from_response_string, \
    format_shop_latlon_decorator, format_shop_working_hours
from utils.general_utils import convert_json_to_dict, convert_dict_to_json
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


def get_shops_information_list(list_city_url: list[str], session: Session):

    list_all_shops_information = []

    for city_url in list_city_url:
        shops_information_response_string = get_shops_information_by_city_response_string(
            shop_information_url=city_url,
            session=session
        )

        string_json_shops_information_response = extract_json_information_from_response_string(
            cities_information_response_string=shops_information_response_string
        )

        dict_shops_information_response = convert_json_to_dict(
            json_object=string_json_shops_information_response
        )

        print(dict_shops_information_response)

        list_shops_information = fetch_list_shops_information(dict_shops_information_response)

        list_all_shops_information += list_shops_information

    return list_all_shops_information





def fetch_list_shops_information(dict_shops_information_response: dict):

    list_shops_information = []

    list_shop_phone_numbers = fetch_shop_phone_numbers_list(
        dict_shops_information_response=dict_shops_information_response
    )

    string_shop_city_name = fetch_shop_city_name(
        dict_shops_information_response=dict_shops_information_response
    )

    for dict_shop_information in dict_shops_information_response['shops']:
        string_shop_name = fetch_shop_name()

        string_shop_address = fetch_shop_address(
            dict_shop_information=dict_shop_information,
            city_name=string_shop_city_name
        )

        list_shop_working_hours = fetch_shop_working_hours(
            dict_shop_information=dict_shop_information
        )

        list_shop_latlon = fetch_shop_latlon(dict_shop_information=dict_shop_information)

        shop_information = {
            "name": string_shop_name,
            "address": string_shop_address,
            "latlon": list_shop_latlon,
            "phones": list_shop_phone_numbers,
            "working_hours": list_shop_working_hours
        }

        list_shops_information.append(shop_information)

    return list_shops_information


def fetch_shop_name():
    return "Японский Домик"


@format_shop_working_hours
def fetch_shop_working_hours(dict_shop_information: dict):
    return dict_shop_information['workingHours']


def fetch_shop_phone_numbers_list(dict_shops_information_response: dict):
    return dict_shops_information_response["city"]['callCenterPhoneParameters']['number']


def fetch_shop_address(dict_shop_information: dict, city_name: str):
    shop_address_string = dict_shop_information['address']

    formatted_shop_address_string = city_name + ', ' + shop_address_string

    return formatted_shop_address_string


@format_shop_latlon_decorator
def fetch_shop_latlon(dict_shop_information: dict):
    return dict_shop_information['coord']


def fetch_shop_city_name(dict_shops_information_response: dict):

    return dict_shops_information_response['city']['name']


def get_shops_information_by_city_response_string(
        shop_information_url: str,
        session: Session
) -> str:

    shops_information_response_string = fetch_data(
        url=shop_information_url,
        session=session
    )

    return shops_information_response_string


if __name__ == '__main__':

    session = init_session(headers=headers)

    list_cities_url = get_cities_url_list(session=session)

    list_shops_information  = get_shops_information_list(session=session, list_city_url=list_cities_url)

    print(list_shops_information)

    close_session(session=session)
