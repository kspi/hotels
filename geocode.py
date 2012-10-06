# coding: utf-8

import json
import httplib
from urllib import urlencode

REGION = 'lt'
HOST = 'maps.googleapis.com'
BASE_PATH = '/maps/api/geocode/json'

def geocode(address):
    args = urlencode({
        'address': address,
        'region': REGION,
        'sensor': 'false'
    })
    try:
        conn = httplib.HTTPConnection(HOST)
        conn.request('GET', BASE_PATH + '?' + args)
        r = conn.getresponse()
        assert(r.status == 200)
        s = r.read().decode('utf-8')
        result = json.loads(s)
    finally:
        conn.close()
    return result

print(geocode('Vokiečių g. 2, Vilnius'))
