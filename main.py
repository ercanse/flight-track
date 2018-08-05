import json
import urllib2

from math import sin, cos, sqrt, atan2, radians

home_location_latitude = 52.086280
home_location_longitude = 4.887380

request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}


def process():
    print 'Retrieving list of all flights...'

    url_string = 'https://data-live.flightradar24.com/zones/fcgi/feed.js?' \
                 'bounds=52.26,51.98,4.37,5.31&faa=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&' \
                 'vehicles=0&estimated=1&maxage=14400&gliders=0&stats=1'
    request_headers['Referer'] = url_string

    request = urllib2.Request(url_string, headers=request_headers)
    contents = urllib2.urlopen(request)
    contents = json.load(contents)

    flights = [key for key in contents.iterkeys() if type(contents[key]) == list]
    num_flights = len(flights)
    if num_flights == 0:
        print 'No flights nearby.'
    else:
        print 'Found {} flights'.format(num_flights), '\n'
        for flight in flights:
            get_flight_info(flight)


def get_flight_info(flight_reference):
    print 'Retrieving details for flight with reference ', flight_reference, '\n'

    url_string = 'https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=' + flight_reference
    request_headers['Referer'] = url_string

    request = urllib2.Request(url_string, headers=request_headers)
    contents = urllib2.urlopen(request)
    contents = json.load(contents)

    print_flight_info(contents)

    last_trail = contents['trail'][0]

    get_distance_between_points(last_trail['lat'], last_trail['lng'], home_location_latitude, home_location_longitude)

    print '\n'


def print_flight_info(flight_info):
    print 'Callsign: ', flight_info['identification']['callsign']
    print 'Status: ', flight_info['status']['text']
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
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    print "Distance to home: ", distance


if __name__ == '__main__':
    process()
