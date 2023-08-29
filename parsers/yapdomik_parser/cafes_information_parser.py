from itertools import groupby

from requests import Session

from decorators.format_information_decorator import format_hospital_latlon_decorator
from parsers.yapdomik_parser.cities_url_parser import get_cities_url_list
from parsers.yapdomik_parser.yapdomik_utils import extract_json_information_from_response_string

from utils.general_utils import convert_json_to_dict
from utils.requests_utils import fetch_data, init_browser_session, close_browser_session


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


def get_cafes_information_list(list_city_url: list[str], browser_session: Session):

    list_all_cafes_information = []

    for city_url in list_city_url:
        cafes_information_response_string = get_cafes_information_response_by_city(
            cafe_information_url=city_url,
            browser_session=browser_session
        )

        string_json_cafes_information_response = extract_json_information_from_response_string(
            cities_information_response_string=cafes_information_response_string
        )

        dict_cafes_information_response = convert_json_to_dict(
            json_object=string_json_cafes_information_response
        )

        print(dict_cafes_information_response)

        list_cafes_information = fetch_list_cafes_information(dict_cafes_information_response)

        list_all_cafes_information += list_cafes_information

    return list_all_cafes_information


def fetch_list_cafes_information(dict_cafes_information_response: dict) -> list[dict]:

    list_cafes_information = []

    list_cafe_cafe_numbers = _get_cafe_phone_numbers(
        dict_cafes_information_response=dict_cafes_information_response
    )

    string_cafe_city_name = _fetch_cafe_city_name(
        dict_cafes_information_response=dict_cafes_information_response
    )

    for dict_cafe_information in dict_cafes_information_response['cafes']:
        string_cafe_name = _get_cafe_name()

        string_cafe_address = _get_cafe_cafe_address(
            dict_cafe_information=dict_cafe_information,
            string_city_name=string_cafe_city_name
        )

        list_cafe_working_hours = _get_cafe_working_hours(
            dict_cafe_information=dict_cafe_information
        )

        list_cafe_latlon = _get_cafe_latlon(
            dict_cafe_information=dict_cafe_information
        )

        dict_cafe_information = _generate_cafe_information_dict(
            string_cafe_name=string_cafe_name,
            string_cafe_address=string_cafe_address,
            list_cafe_latlon=list_cafe_latlon,
            list_cafe_phone_numbers=list_cafe_cafe_numbers,
            list_cafe_working_hours=list_cafe_working_hours
        )

        list_cafes_information.append(dict_cafe_information)

    return list_cafes_information


def _generate_cafe_information_dict(
    string_cafe_name: str,
    string_cafe_address: str,
    list_cafe_latlon: list[float, float],
    list_cafe_phone_numbers: list[str],
    list_cafe_working_hours: list[str]
) -> dict:

    dict_cafe_information = {
        "name": string_cafe_name,
        "address": string_cafe_address,
        "latlon": list_cafe_latlon,
        "phones": list_cafe_phone_numbers,
        "working_hours": list_cafe_working_hours
    }

    return dict_cafe_information


def _get_cafe_name() -> str:
    string_cafe_name = _fetch_cafe_name()

    return string_cafe_name


def _fetch_cafe_name() -> str:
    return "Японский Домик"


def _get_cafe_working_hours(dict_cafe_information: dict) -> list:
    list_cafe_working_hours = _fetch_cafe_working_hours(
        dict_cafe_information=dict_cafe_information
    )

    formatted_list_cafe_working_hours = _format_cafe_working_hours(
        list_cafe_working_hours=list_cafe_working_hours
    )

    return formatted_list_cafe_working_hours


def _fetch_cafe_working_hours(dict_cafe_information: dict) -> list:
    return dict_cafe_information['workingHours']


# необходимо отрефакторить
def _format_cafe_working_hours(list_cafe_working_hours: list):
    day_names = {
        1: 'Пн',
        2: 'Вт',
        3: 'Ср',
        4: 'Чт',
        5: 'Пт',
        6: 'Сб',
        7: 'Вс',
    }

    default_hours = [hour for hour in list_cafe_working_hours if hour['type'] == 'default']

    tewo_list = []

    for hour in default_hours:
        temp_dict = {}

        day_name = day_names[hour['day']]

        if hour['from'] is None and hour['to'] is None:

            tewo_list.pop()

            temp_dict = {
                'day': day_name,
                'time': '00:00-00:00'
            }

            tewo_list.append(temp_dict)

        else:
            hours_string = f"{int(hour['from']) // 60 % 24:02d}:{int(hour['from']) % 60:02d}" \
                           f" — {int(hour['to']) // 60 % 24:02d}:{int(hour['to']) % 60:02d}"

            _string = f"{day_name}: {hours_string}"

            temp_dict = {
                'day': day_name,
                'time': hours_string
            }

            tewo_list.append(temp_dict)

    grouped_data = {}

    key_func = lambda x: x['time']

    for key, group in groupby(tewo_list, key_func):
        if key in grouped_data:
            grouped_data[key] = list(group) + grouped_data[key]

        if key not in grouped_data:
            grouped_data[key] = []
            grouped_data[key] += list(group)

    list_cafe_working_hours = []

    if len(grouped_data.keys()) == 2:
        for key, value in grouped_data.items():

            if len(value) > 1:

                first_group_day = value[0]['day']

                last_group_day = value[-1]['day']

                string_working_hours = f"{first_group_day}-{last_group_day} {key}"

            else:
                group_day = value[0]['day']

                string_working_hours = f"{group_day} {key}"

            list_cafe_working_hours.append(string_working_hours)

    else:

        for key, value in grouped_data.items():
            first_group_day = value[0]['day']

            last_group_day = value[-1]['day']

            string_working_hours = f"{first_group_day}-{last_group_day} {key}"

            list_cafe_working_hours.append(string_working_hours)

    return list_cafe_working_hours


def _get_cafe_phone_numbers(dict_cafes_information_response: dict) -> list[str]:

        list_cafe_phone_number = _fetch_cafe_phone_numbers_list(
            dict_cafes_information_response=dict_cafes_information_response
        )

        return list_cafe_phone_number


def _fetch_cafe_phone_numbers_list(dict_cafes_information_response: dict) -> list:
    return dict_cafes_information_response["city"]['callCenterPhoneParameters']['number']


def _get_cafe_cafe_address(dict_cafe_information: dict, string_city_name: str) -> str:
    string_cafe_address = _fetch_cafe_address(
        dict_cafe_information=dict_cafe_information
    )

    formatted_string_cafe_address = _format_cafe_address(
        cafe_address=string_cafe_address,
        string_cafe_city_name=string_city_name)

    return formatted_string_cafe_address


def _fetch_cafe_address(dict_cafe_information: dict) -> str:
    return dict_cafe_information['address']


def _format_cafe_address(cafe_address: str, string_cafe_city_name: str) -> str:
    formatted_string_cafe_address = f"{cafe_address} + ', ' + {string_cafe_city_name}".strip().replace('\u200b', '')

    return formatted_string_cafe_address


def _get_cafe_latlon(dict_cafe_information: dict) -> list[float, float]:

    dict_cafe_latlon = _fetch_cafe_latlon(
        dict_cafe_information=dict_cafe_information
    )

    formatted_list_cafe_latlon = _format_cafe_latlon(
        dict_cafe_latlon=dict_cafe_latlon
    )

    return formatted_list_cafe_latlon


def _fetch_cafe_latlon(dict_cafe_information: dict) -> dict[str, str]:
    return dict_cafe_information['coord']


def _format_cafe_latlon(dict_cafe_latlon: dict) -> list[float, float]:
    list_hospital_latlon = [
        float(dict_cafe_latlon['latitude']),
        float(dict_cafe_latlon['longitude'])
    ]

    return list_hospital_latlon


def _get_cafe_city_name(dict_cafes_information_response: dict) -> str:

    string_cafe_city_name = _fetch_cafe_city_name(
        dict_cafes_information_response=dict_cafes_information_response
    )

    formatted_string_cafe_city_name = _format_cafe_city_name(cafe_city_name=string_cafe_city_name)

    return formatted_string_cafe_city_name


def _fetch_cafe_city_name(dict_cafes_information_response: dict) -> str:

    return dict_cafes_information_response['city']['name'].strip()


def _format_cafe_city_name(cafe_city_name: str) -> str:

    return cafe_city_name.strip()


def get_cafes_information_response_by_city(
        cafe_information_url: str,
        browser_session: Session
) -> str:

    string_cafes_information_response = fetch_data(
        url=cafe_information_url,
        browser_session=browser_session
    )

    return string_cafes_information_response


if __name__ == '__main__':

    browser_session = init_browser_session(headers=headers)

    list_cities_url = get_cities_url_list(browser_session=browser_session)

    list_cafes_information = get_cafes_information_list(browser_session=browser_session, list_city_url=list_cities_url)

    print(list_cafes_information)

    close_browser_session(browser_session=browser_session)
