import functools
import re
import json
from itertools import groupby
from operator import itemgetter

from bs4 import BeautifulSoup


def extract_json_information_from_response_string(cities_information_response_string: str):

    html = BeautifulSoup(cities_information_response_string, 'html.parser')

    json_information = html.find(
        'script',
        string=re.compile(r'window\.initialState')
    ).string

    json_text = re.search(
        r'^\s*window\.initialState\s*=\s*({.*?})\s*\s*$',
        json_information,
        flags=re.DOTALL | re.MULTILINE
    ).group(1)

    return json_text


def format_shop_latlon_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dict_hospital_latlon = func(*args, **kwargs)

        list_hospital_latlon = [
            float(dict_hospital_latlon['latitude']),
            float(dict_hospital_latlon['longitude'])
        ]

        return list_hospital_latlon

    return wrapper


def format_shop_working_hours(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        list_shop_working_hours = func(*args, **kwargs)

        default_hours = [hour for hour in list_shop_working_hours if hour['type'] == 'default']

        if not default_hours:
            print("Часы работы для типа 'default' не найдены.")
        else:
            grouped_hours = {key: list(group) for key, group in groupby(default_hours, key=itemgetter('day'))}

            day_names = {
                1: 'Пн',
                2: 'Вт',
                3: 'Ср',
                4: 'Чт',
                5: 'Пт',
                6: 'Сб',
                7: 'Вс',
            }

            result_strings = []

            for day, hours_list in grouped_hours.items():
                day_ranges = []

                for hour in hours_list:
                    if hour['from'] is None and hour['to'] is None:
                        result_strings.append(f"{day_names[day]}: 00:00 - 00:00")
                    else:
                        hours_string = f"{int(hour['from']) // 60:02d}:{int(hour['from']) % 60:02d} — {int(hour['to']) // 60:02d}:{int(hour['to']) % 60:02d}"
                        day_ranges.append(hours_string)
                        days_string = day_names[day]
                        result_strings.append(f"{days_string} {hours_string}")

            return result_strings

    return wrapper
