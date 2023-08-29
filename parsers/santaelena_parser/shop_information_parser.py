import re

from requests import Session

from config import SANTA_ELENA_BASE_HEADERS
from parsers.santaelena_parser.cities_url_parser import get_cities_url_list
from utils.geocoding_utils import get_place_coordinates_by_address

from utils.requests_utils import fetch_data, init_session, close_session
from bs4 import BeautifulSoup


def get_shops_information_list(list_city_url: list[str], browser_session: Session) -> dict:

    list_all_shops_information = []

    for city_url in list_city_url:
        shops_information_response_string = get_shops_information_by_city_response_string(
            cafe_information_url=city_url,
            browser_session=browser_session
        )

        list_shops_information = fetch_list_shops_information(shops_information_response_string)

        list_all_shops_information += list_shops_information
    
    dict_all_shops_information = {'shops': list_all_shops_information}

    return dict_all_shops_information


def fetch_list_shops_information(shops_information_response_string: str):
    list_shops_information = []

    html = BeautifulSoup(shops_information_response_string, 'html.parser')

    div_elements = html.find_all('div', class_='elementor-widget-wrap')

    string_cafe_city_name = fetch_cafe_city_name(
        html=html
    )

    list_shops_html = [
        div for div in div_elements if
        div.find('h3', class_='elementor-heading-title elementor-size-default')
    ]

    for cafe_html in list_shops_html:

        string_cafe_name = fetch_cafe_name(html=cafe_html)

        list_cafe_phone_numbers = fetch_cafe_phone_numbers_list(
            html=cafe_html
        )

        string_cafe_address = fetch_cafe_address(
            html=cafe_html,
            city_name=string_cafe_city_name
        )

        list_cafe_working_hours = fetch_cafe_working_hours(
            html=cafe_html
        )

        list_cafe_latlon = fetch_cafe_latlon(
            cafe_address=string_cafe_address
        )

        cafe_information = {
            "name": string_cafe_name,
            "address": string_cafe_address,
            "latlon": list_cafe_latlon,
            "phones": list_cafe_phone_numbers,
            "working_hours": list_cafe_working_hours
        }

        list_shops_information.append(cafe_information)

    return list_shops_information


def fetch_cafe_name(html: BeautifulSoup):

    string_cafe_name = html.find('h3', class_='elementor-heading-title').text.replace('\br', ' ')

    return string_cafe_name


def fetch_cafe_working_hours(html: BeautifulSoup):

    list_p_cafe_working_hours = html.find('div', class_='elementor-text-editor elementor-clearfix')

    test = list_p_cafe_working_hours.find(
        lambda tag: tag.name in ['p', 'h4'] and 'Horario de atención' in tag.get_text()
    )

    hello = test.find_next_siblings('p')

    working_days = [i.text.strip() for i in hello]

    if not working_days:
        return test.text.split(':')[1].strip()

    return working_days


def extract_phone_number(string_cafe):

    phone_pattern = re.compile(re.compile(r'\d{3}\s*\d{3}\s*\d{4}|\d{7}\s*ext\s*\d{4}|\d{7}\s*Ext\s*\d{4}'))

    for paragraph in string_cafe.find_all(lambda tag: tag.name in ['p', 'h4']):
            match = phone_pattern.search(paragraph.get_text())
            if match:
                return match.group(0)


def fetch_cafe_phone_numbers_list(html: BeautifulSoup):

    string_cafe = html.find('div', class_='elementor-text-editor elementor-clearfix')

    string_phone_number = extract_phone_number(string_cafe)

    return string_phone_number


def fetch_cafe_address(html: BeautifulSoup, city_name: str):

    string_cafe = html.find('div', class_='elementor-text-editor elementor-clearfix')

    string_cafe_address = string_cafe.find(lambda tag: tag.name in ['p', 'h4'] and 'Dirección' in tag.get_text())

    if string_cafe_address.name == 'h4':

        return city_name + ", " + string_cafe_address.find_next('p').text.strip()

    return city_name + ", " + string_cafe_address.text.split(':')[1].strip()


def fetch_cafe_latlon(cafe_address: str):
    dict_coordinates = get_place_coordinates_by_address(place_address=cafe_address)

    if dict_coordinates is not None:
        return [dict_coordinates['latitude'], dict_coordinates['longitude']]


def fetch_cafe_city_name(html: BeautifulSoup) -> str:

    string_cafe_city_name = html.find('h2', class_='elementor-heading-title elementor-size-default').text.split()[-1]

    return string_cafe_city_name


def get_shops_information_by_city_response_string(
        cafe_information_url: str,
        browser_session: Session
) -> str:

    shops_information_response_string = fetch_data(
        url=cafe_information_url,
        browser_session=browser_session
    )

    return shops_information_response_string


if __name__ == '__main__':

    browser_session = init_session(headers=SANTA_ELENA_BASE_HEADERS)

    list_cities_url = get_cities_url_list(browser_session=browser_session)

    list_shops_information = get_shops_information_list(browser_session=browser_session, list_city_url=list_cities_url)

    print(list_shops_information)

    close_session(browser_session=browser_session)
