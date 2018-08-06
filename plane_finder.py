import json
import re
import urllib2

from math import sin, cos, sqrt, atan2, radians

home_location_latitude = 52.086280
home_location_longitude = 4.887380

all_flights_url = 'https://planefinder.net/endpoints/update.php'
flight_metadata_url = 'https://planefinder.net/api/api.php?r=aircraftMetadata&adshex={}&flightno={}'
flight_position_url = 'https://planefinder.net/api/api.php?r=planePositions&adshex={}&flightno={}'

request_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'None',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'planefinder.net',
    'Origin': 'https://planefinder.net',
    'Referer': 'https://planefinder.net',
}


def process():
    print 'Retrieving list of all flights...'

    request = urllib2.Request(all_flights_url, headers=request_headers)
    contents = dict()
    try:
        contents = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.fp.read()
        exit(1)

    contents = json.load(contents)
    flights = []

    for planes_list in contents['planes'].values():
        for ads_hex, flight_info in planes_list.iteritems():
            if not flight_info[0] == 'GLID' and not flight_info[1] == 'NO-REG':
                if re.match('^\d{1,2}\.\d+$', flight_info[3]):
                    try:
                        flight_latitude = float(flight_info[3])
                        flight_longitude = float(flight_info[4])
                    except ValueError:
                        continue

                    if 51 <= flight_latitude <= 53 and 4 <= flight_longitude <= 5.5:
                        distance_to_home = get_distance_between_points(
                            home_location_latitude, home_location_longitude, flight_latitude, flight_longitude)

                        try:
                            latitude = float(flight_info[3])
                            longitude = float(flight_info[4])
                        except ValueError:
                            continue

                        if 51 <= latitude <= 53 and 4 <= longitude <= 5.5:
                            print ads_hex, flight_info
                            print 'Altitude: {} feet, heading: {} degrees, speed: {} knots'.format(
                                flight_info[5], flight_info[6], flight_info[7])

                            flights.append({
                                'ads_hex': ads_hex,
                                'aircraft_model': flight_info[0],
                                'flight_number': flight_info[2],
                                'altitude': flight_info[5],
                                'heading': flight_info[6],
                                'speed': flight_info[7],
                                'distance_to_home': distance_to_home
                            })

    flights = sorted(flights, key=lambda k: k['distance_to_home'])
    return flights


def get_flight_info(ads_hex, flight_no):
    flight_info = get_flight_metadata(ads_hex, flight_no)
    flight_position = get_flight_position(ads_hex, flight_no)

    print flight_info
    print flight_position

    flight_latitude = float(flight_position[0])
    flight_longitude = float(flight_position[1])
    distance_to_home = get_distance_between_points(
        home_location_latitude, home_location_longitude, flight_latitude, flight_longitude)

    image_src = ''
    if 'photos' in flight_info and flight_info['photos'] is not None:
        image_src = flight_info['photos'][0]['fullPath']

    departure_airport_string = ''
    destination_airport_string = ''
    if flight_info['flightData']['routing'] is not None:
        departure_airport_ref = flight_info['flightData']['routing'][0]
        destination_airport_ref = flight_info['flightData']['routing'][1]
        departure_airport_city = flight_info['airportDetail'][departure_airport_ref]['airportCity']
        departure_airport_name = flight_info['airportDetail'][departure_airport_ref]['airportName']
        destination_airport_city = flight_info['airportDetail'][destination_airport_ref]['airportCity']
        destination_airport_name = flight_info['airportDetail'][destination_airport_ref]['airportName']

        departure_airport_string = '{} ({})'.format(departure_airport_name, departure_airport_city)
        destination_airport_string = '{} ({})'.format(destination_airport_name, destination_airport_city)

    return {
        'aircraft_type': flight_info['aircraftData']['aircraftFullType'],
        'departure_airport': departure_airport_string,
        'destination_airport': destination_airport_string,
        'altitude': flight_info['dynamic']['selectedAltitude'],
        'heading': flight_info['dynamic']['trackAngle'],
        'speed': flight_info['dynamic']['trueAirSpeed'],
        'distance_to_home': distance_to_home,
        'image_src': image_src
    }


def get_flight_metadata(ads_hex, flight_no):
    print 'Retrieving details for flight with flight no ', flight_no, '\n'

    url_string = flight_metadata_url.format(ads_hex, flight_no)

    request = urllib2.Request(url_string, headers=request_headers)
    contents = urllib2.urlopen(request)
    contents = json.load(contents)

    return contents['payload']


def get_flight_position(ads_hex, flight_no):
    print 'Retrieving details for flight with flight no ', flight_no, '\n'

    url_string = flight_position_url.format(ads_hex, flight_no)

    request = urllib2.Request(url_string, headers=request_headers)
    contents = urllib2.urlopen(request)
    contents = json.load(contents)

    return contents['payload'][0]


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
