import re

from requests import Session

from decorators.format_information_decorator import format_hospital_latlon_decorator
from parsers.santaelena_parser.cities_url_parser import get_cities_url_list

from utils.general_utils import convert_json_to_dict, convert_dict_to_json
from utils.requests_utils import fetch_data, init_session, close_session
from bs4 import BeautifulSoup

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

        list_shops_information = fetch_list_shops_information(shops_information_response_string)

        list_all_shops_information += list_shops_information

    return list_all_shops_information





def fetch_list_shops_information(shops_information_response_string: str):
    list_shops_information = []

    html = BeautifulSoup(shops_information_response_string, 'html.parser')

    div_elements = html.find_all('div', class_='elementor-widget-wrap')

    list_shops_html = [
        div for div in div_elements if
        div.find('h3', class_='elementor-heading-title elementor-size-default')
    ]

    for shop_html in list_shops_html:

        string_shop_name = fetch_shop_name(html=shop_html)

        list_shop_phone_numbers = fetch_shop_phone_numbers_list(
            html=shop_html
        )

        string_shop_city_name = fetch_shop_city_name(
            html=shop_html
        )

        string_shop_address = fetch_shop_address(
            html=html
        )

        list_shop_working_hours = fetch_shop_working_hours(
            html=shop_html
        )

        list_shop_latlon = fetch_shop_latlon({})

        shop_information = {
            "name": string_shop_name,
            "address": string_shop_address,
            "latlon": list_shop_latlon,
            "phones": list_shop_phone_numbers,
            "working_hours": list_shop_working_hours
        }

        list_shops_information.append(shop_information)

    return list_shops_information


def fetch_shop_name(html: BeautifulSoup):

    string_shop_name = html.find('h3', class_='elementor-heading-title').text.replace('\br', ' ')

    return string_shop_name


def fetch_shop_working_hours(html: BeautifulSoup):

    list_p_shop_working_hours = html.find('div', class_='elementor-text-editor elementor-clearfix')

    test = list_p_shop_working_hours.find(
        lambda tag: tag.name in ['p', 'h4'] and 'Horario de atención' in tag.get_text()
    )

    hello = test.find_next_siblings('p')

    working_days = [i.text.strip() for i in hello]

    if working_days == []:
        return test.text.split(':')[1].strip()

    return working_days


def extract_phone_number(string_shop):

    phone_pattern = re.compile(re.compile(r'\d{3}\s*\d{3}\s*\d{4}|\d{7}\s*ext\s*\d{4}|\d{7}\s*Ext\s*\d{4}'))

    for paragraph in string_shop.find_all(lambda tag: tag.name in ['p', 'h4']):
            match = phone_pattern.search(paragraph.get_text())
            if match:
                return match.group(0)


def fetch_shop_phone_numbers_list(html: BeautifulSoup):

    string_shop = html.find('div', class_='elementor-text-editor elementor-clearfix')

    string_phone_number = extract_phone_number(string_shop)

    return string_phone_number


def fetch_shop_address(html: BeautifulSoup):

    string_shop = html.find('div', class_='elementor-text-editor elementor-clearfix')

    string_shop_address = string_shop.find_all(lambda tag: tag.name in ['p', 'h4'] and 'Dirección' in tag.get_text())

    print(string_shop_address)


def fetch_shop_latlon(dict_shop_information: dict):
    pass


def fetch_shop_city_name(html: BeautifulSoup):
    pass


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

    list_shops_information = get_shops_information_list(session=session, list_city_url=list_cities_url)

    print(list_shops_information)

    close_session(session=session)
