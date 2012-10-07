# coding: utf-8
import urllib2
import simplejson
import sys
import csv
import re
import os
from unidecode import unidecode
from PIL import Image
from time import sleep
import StringIO

def get(terms, start=0):
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
           'v=1.0&q={terms}&userip={ip}&start={start}').format(
                start=start,
                ip='84.240.55.160',
                terms=urllib2.quote(terms))

    request = urllib2.Request(url, None, {'Referer': 'http://localhost'})
    response = urllib2.urlopen(request)

    resp = simplejson.load(response)
    results = resp['responseData']['results']
    if results:
        return results[0]['url']
    else:
        return None

def make_terms(title):
    return re.sub(ur'[^a-zA-Z ]', '', unidecode(title).lower()).strip()

def image_filename(title):
    return 'img/hotels/%s.png' % make_terms(title).replace(' ', '-')

if __name__ == '__main__':
    with open('data/hotels.csv', 'r') as f:
        for row in csv.DictReader(f):
            title = row['Pavadinimas']
            terms = make_terms(title) + ' viešbutis'
            imfn = image_filename(title)

            if os.path.exists('site/' + imfn):
                continue

            url = get(terms)
            if not url:
                continue

            try:
                buf = urllib2.urlopen(url).read()
            except urllib2.HTTPError:
                continue

            img = Image.open(StringIO.StringIO(buf))
            img.save('site/' + imfn)

            print(image_filename(title))

            sleep(0.3)
