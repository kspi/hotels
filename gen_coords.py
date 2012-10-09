from normalize_address import normalize_address
from geocode import address_coords
import csv
import json

if __name__ == '__main__':
    with open('coords.json', 'r') as coordsf:
        coords = json.load(coordsf)

    try:
        with open('data/hotels.csv', 'r') as inf:
            r = csv.reader(inf)
            next(r) # skip header
            for row in r:
                addr = row[1].decode('utf-8')
                if addr not in coords:
                    cs = address_coords(addr)
                    if cs:
                        coords[addr] = cs
    finally:
        with open('coords.json', 'w') as coordsf:
            json.dump(coords, coordsf, indent=4)
