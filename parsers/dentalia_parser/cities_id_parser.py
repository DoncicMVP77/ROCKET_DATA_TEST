from requests import Session
from bs4 import BeautifulSoup

from utils.requests_utils import fetch_data, init_session, close_session

hospital_url = 'https://dentalia.com/clinica/'


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


def get_list_cities_id(session: Session):

    hospital_cities_response = get_cities_response(
        url=hospital_url,
        session=session,
    )

    list_cities_id = fetch_cities_id(
        site_response=hospital_cities_response
    )

    return list_cities_id


def fetch_cities_id(site_response: str):

    html = BeautifulSoup(site_response, 'html.parser')

    list_cities = html.find('select', class_='jet-select__control').find_all('option')

    list_cities_id = [cities['value'] if cities['value'] != '' else None for cities in list_cities ]

    return list_cities_id


def get_cities_response(
    url: str,
    session: Session
):

    hospital_cities_response = fetch_data(
        url=url,
        session=session
    )

    return hospital_cities_response


if __name__ == '__main__':

    session = init_session(
        headers=headers
    )

    list_cities_id = get_list_cities_id(
        session=session
    )

    print(list_cities_id)

    close_session(
        session=session
    )

