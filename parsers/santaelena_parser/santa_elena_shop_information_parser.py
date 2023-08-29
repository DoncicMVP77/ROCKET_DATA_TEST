import re
from typing import Union, Optional

from requests import Session

from config import SANTA_ELENA_BASE_HEADERS
from parsers.santaelena_parser.cities_url_parser import get_cities_url_list
from utils.geocoding_utils import get_place_coordinates_by_address

from utils.requests_utils import fetch_data, init_session, close_session
from bs4 import BeautifulSoup, Tag


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

    string_cafe_city_name = _get_cafe_city_name(
        html=html
    )

    list_shops_html = _get_shops_html(html=html)

    for cafe_html in list_shops_html:

        string_cafe_name = _get_cafe_name(html=cafe_html)

        list_cafe_phone_numbers = _get_cafe_phone_numbers(
            html=cafe_html
        )

        string_cafe_address = _get_cafe_address(
            html=cafe_html,
            city_name=string_cafe_city_name
        )

        list_cafe_working_hours = _get_cafe_working_hours(
            html=cafe_html
        )

        list_cafe_latlon = _get_cafe_latlon(
            cafe_address=string_cafe_address
        )

        dict_cafe_information = _generate_shop_information_dict(
            string_cafe_name=string_cafe_name,
            string_cafe_address=string_cafe_address,
            list_cafe_latlon=list_cafe_latlon,
            list_cafe_working_hours=list_cafe_working_hours,
            list_cafe_phone_numbers=list_cafe_phone_numbers
        )

        list_shops_information.append(dict_cafe_information)

    return list_shops_information


def _get_shops_html(html: BeautifulSoup) -> list[BeautifulSoup]:
    page_wrapper_div_elements = html.find_all('div', class_='elementor-widget-wrap')

    list_shops_html = [
        div for div in page_wrapper_div_elements if
        div.find('h3', class_='elementor-heading-title elementor-size-default')
    ]

    return list_shops_html


def _generate_shop_information_dict(
    string_cafe_name: str,
    string_cafe_address: str,
    list_cafe_latlon: list[float, float],
    list_cafe_phone_numbers: list[str],
    list_cafe_working_hours: list[str]
) -> dict:

    cafe_information = {
        "name": string_cafe_name,
        "address": string_cafe_address,
        "latlon": list_cafe_latlon,
        "phones": list_cafe_phone_numbers,
        "working_hours": list_cafe_working_hours
    }

    return cafe_information


def _get_cafe_name(html: BeautifulSoup) -> str:
    string_cafe_name = _fetch_cafe_name(html=html)

    formatted_cafe_name = _format_cafe_name(string_cafe_name=string_cafe_name)

    return formatted_cafe_name


def _fetch_cafe_name(html: BeautifulSoup) -> str:

    string_cafe_name = html.find('h3', class_='elementor-heading-title').text

    return string_cafe_name


def _format_cafe_name(string_cafe_name: str) -> str:

    return string_cafe_name.replace('\br', ' ').strip()


def _get_cafe_working_hours(html: BeautifulSoup) -> list:

    cafe_working_hours = fetch_cafe_working_hours(html=html)

    formatted_list_working_hours = _format_cafe_working_hours(cafe_working_hours=cafe_working_hours)

    return formatted_list_working_hours


def fetch_cafe_working_hours(html: BeautifulSoup) -> Union[str, list]:

    cafe_html = html.find('div', class_='elementor-text-editor elementor-clearfix')

    html_working_hours = cafe_html.find(
        lambda tag: tag.name in ['p', 'h4'] and 'Horario de atención' in tag.get_text()
    )

    p_tag_with_cafe_working_hours = html_working_hours.find_next_siblings('p')

    working_days = [i.text for i in p_tag_with_cafe_working_hours]

    if not working_days:
        return html_working_hours.text.split(':')[1]

    return working_days


def _format_cafe_working_hours(cafe_working_hours: Union[str, list[str]]) -> list:
    if isinstance(cafe_working_hours, list):
        formatted_list_working_hours = [
            working_hours.strip().replace('/', '-')
            for working_hours in cafe_working_hours
        ]

        return formatted_list_working_hours

    formatted_list_working_hours = [cafe_working_hours.strip().rstrip('.')]

    return formatted_list_working_hours


def _get_cafe_phone_numbers(html: BeautifulSoup):

    string_phone_number = _fetch_cafe_phone_numbers(html=html)

    formatted_list_phone_number = _format_phone_number(string_phone_number=string_phone_number)

    return formatted_list_phone_number


def _fetch_cafe_phone_numbers(html: BeautifulSoup):

    string_cafe = html.find('div', class_='elementor-text-editor elementor-clearfix')

    string_phone_number = _extract_phone_number(string_cafe)

    return string_phone_number


def _extract_phone_number(string_cafe: Tag) -> str:

    phone_pattern = re.compile(re.compile(r'\d{3}\s*\d{3}\s*\d{4}|\d{7}\s*ext\s*\d{4}|\d{7}\s*Ext\s*\d{4}'))

    for paragraph in string_cafe.find_all(lambda tag: tag.name in ['p', 'h4']):
            match = phone_pattern.search(paragraph.get_text())
            if match:
                return match.group(0)


def _format_phone_number(string_phone_number: str) -> list[str]:

    return [string_phone_number]


def _get_cafe_address(html: BeautifulSoup, city_name: str) -> str:

    tag_cafe_address = _fetch_cafe_address(html=html)

    formatted_string_cafe_address = _format_cafe_address(
        tag_cafe_address=tag_cafe_address,
        city_name=city_name
    )

    return formatted_string_cafe_address


def _fetch_cafe_address(html: BeautifulSoup) -> Tag:

    string_cafe = html.find('div', class_='elementor-text-editor elementor-clearfix')

    tag_cafe_address = string_cafe.find(lambda tag: tag.name in ['p', 'h4'] and 'Dirección' in tag.get_text())

    return tag_cafe_address


def _format_cafe_address(tag_cafe_address: Tag, city_name: str) -> str:

    if tag_cafe_address.name == 'h4':

        return city_name + ", " + tag_cafe_address.find_next('p').text.strip()

    return city_name + ", " + tag_cafe_address.text.split(':')[1].strip()


def _get_cafe_latlon(cafe_address: str) -> Union[None, list[float, float]]:

    dict_cafe_latlon = _fetch_cafe_latlon(cafe_address=cafe_address)

    formatted_list_cafe_latlon = _format_cafe_latlon(dict_cafe_latlon=dict_cafe_latlon)

    return formatted_list_cafe_latlon


def _fetch_cafe_latlon(cafe_address: str) -> dict:
    dict_coordinates = get_place_coordinates_by_address(place_address=cafe_address)

    return dict_coordinates


def _format_cafe_latlon(dict_cafe_latlon: Optional[dict]) -> Union[None, list[float, float]]:
    if dict_cafe_latlon is not None:
        return [dict_cafe_latlon['latitude'], dict_cafe_latlon['longitude']]


def _get_cafe_city_name(html: BeautifulSoup) -> str:

    string_cafe_city_name = _fetch_cafe_city_name(html=html)

    formatted_string_cafe_city_name = _format_cafe_city_name(
        string_cafe_city_name=string_cafe_city_name
    )

    return formatted_string_cafe_city_name


def _fetch_cafe_city_name(html: BeautifulSoup) -> str:

    string_cafe_city_name = html.find(
        'h2', class_='elementor-heading-title elementor-size-default'
    ).text.split()[-1]

    return string_cafe_city_name


def _format_cafe_city_name(string_cafe_city_name: str) -> str:
    return string_cafe_city_name.strip()


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
