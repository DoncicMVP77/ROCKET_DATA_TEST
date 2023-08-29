from config import SANTA_ELENA_BASE_HEADERS
from parsers.santaelena_parser.cities_url_parser import get_cities_url_list
from parsers.santaelena_parser.santa_elena_shop_information_parser import get_shops_information_list
from utils.requests_utils import close_session, init_session


def main_santa_elena_parser_handler():
    browser_session = init_session(headers=SANTA_ELENA_BASE_HEADERS)

    list_cities_url = get_cities_url_list(browser_session=browser_session)

    list_shops_information = get_shops_information_list(
        browser_session=browser_session,
        list_city_url=list_cities_url
    )

    close_session(browser_session=browser_session)
    
    return list_shops_information

if __name__ == '__main__':
    main_santa_elena_parser_handler()
    
    