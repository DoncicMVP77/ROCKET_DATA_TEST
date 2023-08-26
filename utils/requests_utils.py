from typing import Optional, Union

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from urllib3 import Retry

from utils.general_utils import is_json_content

base_headers = {}

base_cookies = {}

base_proxies = {
    'https': f'http://0bcb607861:c81604b0c6@95.31.211.120:30069',
    #'http': f'http://0bcb607861:c81604b0c6@95.31.211.120:30069',
}


def fetch_data(
    session: Session,
    url: str,
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
    params: Optional[dict] = None
) -> Union[dict, str]:

    session.headers.update(headers) if headers is not None else None

    session.cookies.update(cookies) if cookies is not None else None

    try:
        response = session.get(url=url, params=params)
        response.raise_for_status()
    except HTTPError as ex:
        print(ex.response)
    else:
        if is_json_content(response):
            return response.json()

        return response.text


def init_session(
    headers: Optional[dict] = None,
    cookies: Optional[dict] = None,
    proxies: Optional[dict] = None
) -> Session:

    session = Session()

    retries = Retry(
        total=10,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504, 403, 407, 401],
        redirect=30
    )

    session.mount('https://', HTTPAdapter(max_retries=retries, pool_maxsize=30))
    session.mount('http://', HTTPAdapter(max_retries=retries, pool_maxsize=30))

    session.headers.update(headers if headers is not None else base_headers)
    session.cookies.update(cookies if cookies is not None else base_cookies)

    session.proxies.update(cookies if cookies is not None else base_cookies)

    return session


def close_session(session: Session) -> None:

    session.close()
