from requests import Session

from config import DENTALIA_GET_HOSPITAL_BY_CITY_DATA, DENTALIA_BASE_HEADERS, DENTALIA_GET_HOSPITAL_BY_CITY_URL
from parsers.dentalia_parser.cities_id_parser import get_list_cities_id
from utils.requests_utils import init_session, close_session, fetch_data


def get_list_hospitals_id_and_latlon(
        list_cities_id: list[str],
        browser_session: Session
) -> list[dict]:

    list_all_hospital_id_and_latlon = []

    for cities_id in list_cities_id:

        dict_hospital_list_api_response = _get_hospital_list_response_by_city_id(
            cities_id=cities_id, browser_session=browser_session
        )

        list_all_hospital_id_and_latlon += _fetch_hospital_id_and_latlon(dict_hospital_list_api_response)

    return list_all_hospital_id_and_latlon


def _fetch_hospital_id_and_latlon(dict_hospital_response_dict: dict) -> list[dict]:

    list_hospital_id_and_latlon = [
        {
            'hospital_id': hospital['id'],
            'latlon': hospital['latLang']
        } for hospital in dict_hospital_response_dict['markers']
    ]

    return list_hospital_id_and_latlon


def _get_hospital_list_response_by_city_id(
        cities_id: str,
        browser_session: Session
) -> dict:
    DENTALIA_GET_HOSPITAL_BY_CITY_DATA['query[_tax_query_estados]'] = cities_id

    hospital_cities_response = fetch_data(
        url=DENTALIA_GET_HOSPITAL_BY_CITY_URL,
        browser_session=browser_session,
        params=DENTALIA_GET_HOSPITAL_BY_CITY_DATA
    )

    return hospital_cities_response


if __name__ == '__main__':

    browser_session = init_session(
        headers=DENTALIA_BASE_HEADERS
    )

    list_cities_id = get_list_cities_id(browser_session=browser_session)

    list_hospital_id = get_list_hospitals_id_and_latlon(list_cities_id, browser_session)

    print(list_hospital_id)

    close_session(browser_session=browser_session)
