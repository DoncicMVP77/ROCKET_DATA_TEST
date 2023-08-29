import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

GOOGLE_GEOCODING_API_KEY = os.getenv('GOOGLE_GEOCODING_API_KEY')

YAPDOMIK_BASE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://omsk.yapdomik.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 '
                  'Safari/537.36',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

YAPDOMIK_CITIES_URL = 'https://omsk.yapdomik.ru/about'

YAPDOMIK_CITIES_URL_FORMAT = 'https://{city_alias}.yapdomik.ru/about'

SANTA_ELENA_BASE_HEADERS = {
    'authority': 'www.santaelena.com.co',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'referer': 'https://www.santaelena.com.co/tiendas-pasteleria/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

SANTA_ELENA_CITIES_URL = 'https://www.santaelena.com.co/tiendas-pasteleria/'

SANTA_ELENA_CITIES_URL_FORMAT = 'https://www.santaelena.com.co/tiendas-pasteleria/'

DENTALIA_BASE_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
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

DENTALIA_HOPSITAL_CITIES_URL = 'https://dentalia.com/clinica/'

DENTALIA_GET_HOSPITAL_BY_CITY_URL = 'https://dentalia.com/wp-admin/admin-ajax.php'

DENTALIA_GET_HOSPITAL_BY_CITY_DATA = {
    'action': 'jet_smart_filters',
    'provider': 'jet-engine-maps/map',
    'query[_tax_query_estados]': '16',
    'defaults[post_status]': 'publish',
    'defaults[post_type]': 'clinicas',
    'defaults[posts_per_page]': '100',
    'defaults[paged]': '1',
    'defaults[ignore_sticky_posts]': '1',
    'settings[lisitng_id]': '6640',
    'settings[address_field]': 'direccion',
    'settings[add_lat_lng]': '',
    'settings[lat_lng_address_field]': '',
    'settings[posts_num]': '100',
    'settings[auto_center]': 'yes',
    'settings[max_zoom]': '15',
    'settings[custom_center]': '',
    'settings[custom_zoom]': '11',
    'settings[zoom_control]': 'auto',
    'settings[zoom_controls]': 'true',
    'settings[fullscreen_control]': 'true',
    'settings[street_view_controls]': 'true',
    'settings[map_type_controls]': '',
    'settings[posts_query][0][_id]': '593cb36',
    'settings[posts_query][0][tax_query_taxonomy]': 'estados',
    'settings[posts_query][0][tax_query_terms]': '%current_terms|estados%{"context":"default_object"}',
    'settings[meta_query_relation]': 'AND',
    'settings[tax_query_relation]': 'AND',
    'settings[hide_widget_if]': '',
    'settings[popup_width]': '450',
    'settings[popup_offset]': '40',
    'settings[marker_type]': 'icon',
    'settings[marker_image][url]': '',
    'settings[marker_image][id]': '',
    'settings[marker_image][size]': '',
    'settings[marker_icon][value]': 'fas fa-map-marker-alt',
    'settings[marker_icon][library]': 'fa-solid',
    'settings[marker_label_type]': 'post_title',
    'settings[marker_label_field]': '',
    'settings[marker_label_field_custom]': '',
    'settings[marker_label_text]': '',
    'settings[marker_label_format_cb]': '0',
    'settings[marker_label_custom]': '',
    'settings[marker_label_custom_output]': '%s',
    'settings[marker_image_field]': '',
    'settings[marker_image_field_custom]': '',
    'settings[multiple_marker_types]': '',
    'settings[marker_clustering]': 'true',
    'settings[popup_pin]': '',
    'settings[popup_preloader]': '',
    'settings[custom_query]': '',
    'settings[custom_query_id]': '10',
    'settings[labels_by_glossary]': '',
    'settings[date_format]': 'F j, Y',
    'settings[num_dec_point]': '.',
    'settings[num_thousands_sep]': ',',
    'settings[human_time_diff_from_key]': '',
    'settings[num_decimals]': '2',
    'settings[zeroise_threshold]': '3',
    'settings[proportion_divisor]': '10',
    'settings[proportion_multiplier]': '5',
    'settings[proportion_precision]': '0',
    'settings[child_path]': '',
    'settings[attachment_image_size]': 'full',
    'settings[thumbnail_add_permalink]': '',
    'settings[related_list_is_single]': '',
    'settings[related_list_is_linked]': 'yes',
    'settings[related_list_tag]': 'ul',
    'settings[multiselect_delimiter]': ', ',
    'settings[switcher_true]': '',
    'settings[switcher_false]': '',
    'settings[url_scheme]': '',
    'settings[checklist_cols_num]': '1',
    'settings[checklist_divider]': '',
    'settings[user_data_to_get]': 'display_name',
    'props[found_posts]': '65',
    'props[max_num_pages]': '1',
    'props[page]': '1',
}

DENTAIL_FILE_PATH = Path.cwd() / 'static' / 'dentail_hospitals.json'

SANTA_ELENA_FILE_PATH = Path.cwd() / 'static' / 'santa_elena_shops.json'

YAPDOMIK_FILE_PATH = Path.cwd() / 'static' / 'yapdomik_cafes.json'


if __name__ == '__main__':
    print(GOOGLE_GEOCODING_API_KEY)
