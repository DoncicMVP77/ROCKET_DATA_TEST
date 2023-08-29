from config import YAPDOMIK_BASE_HEADERS
from parsers.yapdomik_parser.cafes_information_parser import get_cafes_information_list
from parsers.yapdomik_parser.cities_url_parser import get_cities_url_list
from utils.requests_utils import init_session, close_session


def main_yapdomik_parser_handler():
    browser_session = init_session(headers=YAPDOMIK_BASE_HEADERS)

    list_cities_url = get_cities_url_list(browser_session=browser_session)

    list_cafes_information = get_cafes_information_list(
        browser_session=browser_session,
        list_city_url=list_cities_url
    )

    close_session(browser_session=browser_session)


if __name__ == '__main__':
    main_yapdomik_parser_handler()

