import json
import urllib2

def process():
    print 'Retrieving list of all flights...'

    url_string = 'https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds=52.22,52.03,4.59,5.13&faa=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&vehicles=0&estimated=1&maxage=14400&gliders=0&stats=1'
    request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": url_string,
        "Connection": "keep-alive" 
        }

    request = urllib2.Request(url_string, headers=request_headers)
    contents = urllib2.urlopen(request)
    contents = json.load(contents)

    print contents
    print '\n'

    for key, value in contents.iteritems():
        if type(value) == list:
            get_flight_info(key)

def get_flight_info(flight_reference):
    print 'Retrieving details for flight with reference ', flight_reference

    url_string = 'https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=' + flight_reference
    request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": url_string,
        "Connection": "keep-alive" 
        }

    request = urllib2.Request(url_string, headers=request_headers)
    contents = urllib2.urlopen(request)
    contents = json.load(contents)

    print contents['identification']
    print contents['status']
    print contents['aircraft']['model']
    print '\n'

if __name__ == '__main__':
    process()

