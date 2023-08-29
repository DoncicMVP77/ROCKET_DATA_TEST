import functools
import re


def format_phone_numbers_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        string_hospital_phone_numbers = func(*args, **kwargs)
        list_hospital_phone_numbers = string_hospital_phone_numbers.split('\r')

        list_formatted_phone_numbers = [
            "".join(hospital_phone_number.strip().split())
            for hospital_phone_number in list_hospital_phone_numbers
        ]

        return list_formatted_phone_numbers
    return wrapper


def format_dentalia_hospital_name_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        string_hospital_name = func(*args, **kwargs)

        formatted_hospital_name = 'dentalia ' + string_hospital_name

        return formatted_hospital_name

    return wrapper


def format_hospital_latlon_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dict_hospital_latlon = func(*args, **kwargs)

        list_hospital_latlon = [
            float(dict_hospital_latlon['lat']),
            float(dict_hospital_latlon['lng'])
        ]

        return list_hospital_latlon

    return wrapper


def format_hospital_working_hours_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        string_hospital_working_hours = func(*args, **kwargs)

        formatted_string_hospital_working_hours = re.sub(
            "^\s+|\n|\s+$",
            " ",
            re.sub("^\s+|\r|\s+$", "", string_hospital_working_hours)
        )

        return formatted_string_hospital_working_hours

    return wrapper
