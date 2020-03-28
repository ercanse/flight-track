import json
import urllib.request

import config as location_config

from math import sin, cos, sqrt, atan2, radians
from urllib.error import URLError

home_location_latitude = location_config.location['latitude']
home_location_longitude = location_config.location['longitude']
kmh_per_knot = 1.852
meters_per_foot = 0.3

request_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'None',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'data-live.flightradar24.com',
    'Origin': 'https://www.flightradar24.com',
    'Referer': 'https://www.flightradar24.com/DLH1UW/1d64bf47',
}


def process():
    print('Retrieving list of all flights...')

    url_string = 'https://data-live.flightradar24.com/zones/fcgi/feed.js?' \
                 'bounds=52.26,51.98,4.37,5.31&faa=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&' \
                 'vehicles=0&estimated=1&maxage=14400&gliders=0&stats=1'

    request = urllib.request.Request(url_string, headers=request_headers)
    contents = dict()
    try:
        contents = urllib.request.urlopen(request)
    except URLError as e:
        print(e)
        exit(1)

    contents = json.load(contents)

    flights = list()
    for key, value in contents.items():
        if type(value) == list:
            print(value)
            distance_to_home = get_distance_between_points(value[1], value[2], home_location_latitude,
                                                           home_location_longitude)
            flight_result = dict()
            flight_result['reference'] = key
            flight_result['heading'] = value[3]
            flight_result['altitude'] = "{:.0f}".format(value[4] * meters_per_foot)
            flight_result['speed'] = "{:.0f}".format(value[5] * kmh_per_knot)
            flight_result['aircraft_model'] = value[8]
            flight_result['origin'] = value[11]
            flight_result['destination'] = value[12]
            flight_result['flight_number'] = value[13]
            flight_result['distance_to_home'] = distance_to_home
            flights.append(flight_result)

    flights = sorted(flights, key=lambda k: float(k['distance_to_home']))
    return flights


def get_flight_info(flight_reference):
    print('Retrieving details for flight with reference ', flight_reference, '\n')

    url_string = 'https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=' + flight_reference

    request = urllib.request.Request(url_string, headers=request_headers)
    contents = urllib.request.urlopen(request)
    contents = json.load(contents)

    print_flight_info(contents)

    trail = contents.get('trail', None)
    distance_to_home = speed = altitude = heading = None

    if trail:
        last_trail = contents['trail'][0]
        speed = last_trail['spd']
        altitude = last_trail['alt']
        heading = last_trail['hd']
        distance_to_home = get_distance_between_points(last_trail['lat'], last_trail['lng'], home_location_latitude,
                                                       home_location_longitude)

    print('\n')

    aircraft_model = ''
    origin = ''
    destination = ''
    image_src = ''
    if contents['aircraft']['model'] is not None:
        aircraft_model = contents['aircraft']['model']['text']
    if contents['airport']['origin'] is not None:
        origin = contents['airport']['origin']['name']
    if contents['airport']['destination'] is not None:
        destination = contents['airport']['destination']['name']
    if contents['aircraft']['images'] is not None:
        image_src = contents['aircraft']['images']['thumbnails'][0]['src']

    return {
        'aircraft_model': aircraft_model,
        'origin': origin,
        'destination': destination,
        'altitude': "{:.0f}".format(altitude * meters_per_foot),
        'heading': heading,
        'speed': "{:.0f}".format(speed * kmh_per_knot),
        'distance_to_home': distance_to_home,
        'image_src': image_src
    }


def print_flight_info(flight_info):
    print('Callsign: ', flight_info['identification']['callsign'])
    print('Status: ', flight_info['status']['text'])
    if flight_info['aircraft']['model'] is not None:
        print('Aircraft model: ', flight_info['aircraft']['model']['text'])
    if 'name' in flight_info['aircraft']:
        print('Airline: ', flight_info['airline']['name'])
    print('\n')
    if flight_info['airport']['origin'] is not None:
        print('Origin airport: ', flight_info['airport']['origin']['name'])
    if flight_info['airport']['destination'] is not None:
        print('Destination airport: ', flight_info['airport']['destination']['name'])
    print('\n')
    last_trail = flight_info['trail'][0]
    print('Speed: {} knots, altitude: {} feet, heading: {} degrees'.format(last_trail['spd'], last_trail['alt'],
                                                                           last_trail['hd']))


def get_distance_between_points(lat1, lon1, lat2, lon2):
    earth_radius = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    delta_longitude = lon2 - lon1
    delta_latitude = lat2 - lat1

    a = sin(delta_latitude / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_longitude / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c
    distance = "{:.2f}".format(distance)

    print("Distance to home: ", distance)
    return distance


if __name__ == '__main__':
    process()
