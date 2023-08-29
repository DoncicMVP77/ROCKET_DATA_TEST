from config import DENTALIA_HOPSITAL_CITIES_URL, DENTALIA_BASE_HEADERS
from parsers.dentalia_parser.cities_id_parser import get_list_cities_id
from parsers.dentalia_parser.hospital_id_and_latlon_parser import get_list_hospitals_id_and_latlon
from parsers.dentalia_parser.hospital_information_parser import get_list_hospital_information
from utils.general_utils import convert_dict_to_json, write_to_json_file
from utils.requests_utils import init_session, close_session


def main_dentalia_parser_handler():
    browser_session = init_session(
        headers=DENTALIA_BASE_HEADERS
    )

    list_cities_id = get_list_cities_id(
        browser_session=browser_session
    )

    list_hospital_id_and_latlon = get_list_hospitals_id_and_latlon(
        browser_session=browser_session,
        list_cities_id=list_cities_id
    )

    list_hospital_information = get_list_hospital_information(
        list_hospitals_id_and_latlon=list_hospital_id_and_latlon,
        browser_session=browser_session
    )

    close_session(
        browser_session=browser_session
    )

    return list_hospital_information


if __name__ == '__main__':

    hospital_information_dict = main_dentalia_parser_handler()

    print(hospital_information_dict)
