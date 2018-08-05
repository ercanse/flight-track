import json
import urllib2

from math import sin, cos, sqrt, atan2, radians

home_location_latitude = 52.086280
home_location_longitude = 4.887380

request_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'data-live.flightradar24.com',
    'Origin': 'https://www.flightradar24.com',
    'Referer': 'https://www.flightradar24.com/DLH1UW/1d64bf47',
}


def process():
    print 'Retrieving list of all flights...'

    url_string = 'https://data-live.flightradar24.com/zones/fcgi/feed.js?' \
                 'bounds=52.26,51.98,4.37,5.31&faa=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&' \
                 'vehicles=0&estimated=1&maxage=14400&gliders=0&stats=1'

    request = urllib2.Request(url_string, headers=request_headers)
    contents = dict()
    try:
        contents = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.fp.read()
        exit(1)

    contents = json.load(contents)

    flight_results = list()
    for key, value in contents.items():
        if type(value) == list:
            flight_result = dict()
            flight_result['reference'] = key
            flight_result['heading'] = value[3]
            flight_result['altitude'] = value[4]
            flight_result['speed'] = value[5]
            flight_result['aircraft_model'] = value[8]
            flight_result['origin'] = value[11]
            flight_result['destination'] = value[12]
            flight_results.append(flight_result)

    return flight_results

    # num_flights = len(flights)
    # if num_flights == 0:
    #     print 'No flights nearby.'
    # else:
    #     print 'Found {} flights'.format(num_flights), '\n'
    #     for flight in flights:
    #         get_flight_info(flight)


def get_flight_info(flight_reference):
    print 'Retrieving details for flight with reference ', flight_reference, '\n'

    url_string = 'https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=' + flight_reference

    request = urllib2.Request(url_string, headers=request_headers)
    contents = urllib2.urlopen(request)
    contents = json.load(contents)

    print_flight_info(contents)

    last_trail = contents['trail'][0]

    distance_to_home = get_distance_between_points(last_trail['lat'], last_trail['lng'], home_location_latitude,
                                                   home_location_longitude)

    print '\n'

    contents['position_info'] = last_trail
    contents['distance_to_home'] = distance_to_home
    contents['image_src'] = contents['aircraft']['images']['thumbnails'][0]['src']

    return contents


def print_flight_info(flight_info):
    print 'Callsign: ', flight_info['identification']['callsign']
    print 'Status: ', flight_info['status']['text']
    if flight_info['aircraft']['model'] is not None:
        print 'Aircraft model: ', flight_info['aircraft']['model']['text']
    print 'Airline: ', flight_info['airline']['name']
    print '\n'
    if flight_info['airport']['origin'] is not None:
        print 'Origin airport: ', flight_info['airport']['origin']['name']
    if flight_info['airport']['destination'] is not None:
        print 'Destination airport: ', flight_info['airport']['destination']['name']
    print '\n'
    last_trail = flight_info['trail'][0]
    print 'Speed: {} knots, altitude: {} feet, heading: {} degrees'.format(last_trail['spd'], last_trail['alt'],
                                                                           last_trail['hd'])


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

    print "Distance to home: ", distance
    return distance


if __name__ == '__main__':
    process()
