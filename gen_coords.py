from normalize_address import normalize_address
from geocode import address_coords
from codecs import open
import csv
import json

if __name__ == '__main__':
    with open('coords.json', 'r', encoding='utf-8') as coordsf:
        coords = json.load(coordsf)

    try:
        with open('data/hotels.csv', 'r', encoding='utf-8') as inf:
            r = csv.reader(inf)
            next(r) # skip header
            for row in r:
                addr = row[1]
                if addr not in coords:
                    cs = address_coords(addr)
                    if cs:
                        coords[addr] = cs
    finally:
        with open('coords.json', 'w', encoding='utf-8') as coordsf:
            json.dump(coords, coordsf, indent=4, ensure_ascii=False)
