# coding: utf-8
import csv
import json
import os
from codecs import open

largest = 0
count = 0
good_count = 0
hotels = {}

with open('coords.json', 'r', encoding='utf-8') as coordsf:
    coords = json.load(coordsf)

with open('data/hotels.csv', 'r') as f:
    for row in csv.DictReader(f):
        row = {k.decode('utf-8'): v.decode('utf-8') for k, v in row.items()}

        count += 1
        name = row[u'Pavadinimas']
        address = row[u'Veiklos vykdymo vieta']
        rank = int(row[u'Klasė'].replace('*', ''))

        cs = coords.get(address, None)
        if cs:
            good_count += 1

        try:
            size = int(row[u'Vietų skaičius'])
        except ValueError:
            size = None

        if size > largest:
            largest = size

        
        del row[u'Pavadinimas']
        del row[u'Veiklos vykdymo vieta']
        hotel = {
            'name': name,
            'address': address,
            'rank': rank,
            'size': size,
            'info': row,
            'coords': cs,
            'halls': [],
        }

        hotels[name] = hotel


with open('data/halls.csv', 'r') as f:
    for row in csv.DictReader(f):
        row = {k.decode('utf-8'): v.decode('utf-8') for k, v in row.items()}

        hotel_name = row[u'Viešbutis']
        if hotel_name not in hotels:
            continue

        name = row[u'Salė']
        configs = []
        configs_str = row[u'Viet. išdėst. ir sk.']
        for cfgs in configs_str.split(';'):
            cname, people = cfgs.rsplit(':', 1)
            configs.append({
                'name': cname.strip(),
                'people': int(people),
            })

        hardware = row[u'Įranga'].split(', ')

        hall = {
            'name': name,
            'configurations': configs,
            'hardware': hardware,
        }
        hall.update(row)

        hotel = hotels[hotel_name]
        hotel['halls'].append(hall)
        

with open('site/js/data.js', 'w', encoding='utf-8') as f:
    f.write(u'hotels = (')
    json.dump(sorted(list(hotels.values()), key=lambda x: x['size']), f, indent=4, ensure_ascii=False)
    f.write(u');\n')

    f.write(u'largest_hotel_size = %s;\n' % json.dumps(largest))


print(u'Good: %d/%d' % (good_count, count))
