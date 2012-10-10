import json
import csv
from codecs import open

with open('coords.json', 'r', encoding='utf-8') as coordsf:
    coords = json.load(coordsf)

with open('data/coords.csv', 'w') as outf:
    w = csv.writer(outf, lineterminator='\n')
    w.writerow(['Existing address', 'Normalized address', 'Latitude', 'Longitude'])
    for addr, d in coords.items():
        row = (addr, d['normalized'], d['lat'], d['lng'])
        w.writerow([unicode(v).encode('utf-8') for v in row])
