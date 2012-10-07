# coding: utf-8

import json
import httplib
from urllib import urlencode
import lithuanian
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
    sleep(0.1)

    return result


def coords(address):
    """Returns dict with lat and lng of address."""
    for variant in lithuanian.address_variants(address):
        result = geocode(variant)
        status = result['status']
        if status != 'ZERO_RESULTS':
            if status != 'OK':
                raise GeocodeException(status)
            break
    else:
        return None

    r = result['results'][0]
    cs = r['geometry']['location']
    return cs
