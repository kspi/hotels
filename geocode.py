# coding: utf-8

import json
import httplib
from urllib import urlencode
from normalize_address import normalize_address
from time import sleep

REGION = u'lt'
HOST = u'maps.googleapis.com'
BASE_PATH = u'/maps/api/geocode/json'

class GeocodeException(Exception):
    pass

def geocode(address):
    args = urlencode({
        u'address': address.encode('utf-8'),
        u'region': REGION,
        u'sensor': u'false'
    })
    try:
        conn = httplib.HTTPConnection(HOST)
        conn.request('GET', BASE_PATH + u'?' + args)
        r = conn.getresponse()
        assert(r.status == 200)
        s = r.read().decode('utf-8')
        result = json.loads(s)
    finally:
        conn.close()

    # Throttle due to geocode query limit.
    sleep(0.3)

    return result


def address_coords(address):
    """Returns dict with lat and lng of address."""
    print u'Geocoding {}'.format(address).encode('utf-8')
    for variant in normalize_address(address):
        result = geocode(variant)
        status = result['status']
        print u'    {}: {}'.format(variant, status).encode('utf-8')
        if status != 'ZERO_RESULTS':
            if status != 'OK':
                raise GeocodeException(status)
            break
    else:
        return None

    r = result['results'][0]
    cs = r['geometry']['location']
    cs['normalized'] = variant
    return cs
