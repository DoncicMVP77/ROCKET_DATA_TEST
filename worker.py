from pathlib import Path

from config import DENTAIL_FILE_PATH, SANTA_ELENA_FILE_PATH, YAPDOMIK_FILE_PATH
from parsers.dentalia_parser.dentalia_main_parser import main_dentalia_parser_handler
from parsers.santaelena_parser.santa_elena_main_parser import main_santa_elena_parser_handler
from parsers.yapdomik_parser.yapdomik_main_parser import main_yapdomik_parser_handler
from utils.general_utils import convert_dict_to_json
from utils.storage_utils import save_json


def worker_handler():
    dict_hospitals_information = main_dentalia_parser_handler()

    json_hospitals_information = convert_dict_to_json(dict_hospitals_information)

    save_json(json_object=json_hospitals_information, path_object=DENTAIL_FILE_PATH)
    dict_shops_information = main_santa_elena_parser_handler()

    json_shops_information = convert_dict_to_json(dict_shops_information)

    save_json(json_object=json_shops_information, path_object=SANTA_ELENA_FILE_PATH)

    dict_cafes_information = main_yapdomik_parser_handler()

    json_cafes_information = convert_dict_to_json(dict_cafes_information)

    save_json(json_object=json_cafes_information, path_object=YAPDOMIK_FILE_PATH)


if __name__ == '__main__':
    worker_handler()
