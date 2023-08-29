from geopy.geocoders import GoogleV3

from config import GOOGLE_GEOCODING_API_KEY


def get_place_coordinates_by_address(place_address: str):

    geolocator = GoogleV3(api_key=GOOGLE_GEOCODING_API_KEY)

    location = geolocator.geocode(place_address)

    if location:
        return {'latitude': location.latitude, 'longitude': location.longitude}


if __name__ == '__main__':
    print(get_place_coordinates_by_address('47 W 13th St, New York'))

