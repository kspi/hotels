# coding: utf-8
import csv
import json
from im import image_filename
import os

largest = 0
count = 0
good_count = 0
hotels = {}

with open('data/hotels.csv', 'r') as f:
    for row in csv.DictReader(f):
        count += 1
        name = row['Pavadinimas']
        address = row['Veiklos vykdymo vieta']
        rank = int(row['Klasė'].replace('*', ''))

        try:
            size = int(row['Vietų skaičius'])
        except ValueError:
            size = None

        if size > largest:
            largest = size

        good_count += 1
        
        del row['Pavadinimas']
        del row['Veiklos vykdymo vieta']
        hotel = {
            'name': name,
            'address': address,
            'rank': rank,
            'size': size,
            'info': row,
            'halls': [],
        }

        imagefn = image_filename(name)
        if os.path.exists('site/' + imagefn):
            hotel['image_filename'] = imagefn

        hotels[name] = hotel


with open('data/halls.csv', 'r') as f:
    for row in csv.DictReader(f):
        hotel_name = row['Viešbutis']
        if hotel_name not in hotels:
            continue

        name = row['Salė']
        configs = []
        configs_str = row['Viet. išdėst. ir sk.']
        for cfgs in configs_str.split(';'):
            cname, people = cfgs.rsplit(':', 1)
            configs.append({
                'name': cname.strip(),
                'people': int(people),
            })

        hardware = row['Įranga'].split(', ')

        hall = {
            'name': name,
            'configurations': configs,
            'hardware': hardware,
        }
        hall.update(row)

        hotel = hotels[hotel_name]
        hotel['halls'].append(hall)
        

with open('site/js/data.js', 'w') as f:
    f.write('hotels = (')
    f.write(json.dumps(sorted(list(hotels.values()), key=lambda x: x['size']), indent=4))
    f.write(');\n')

    f.write('largest_hotel_size = %s;\n' % json.dumps(largest))


print('Largest: %d' % largest)
print('Good: %d/%d' % (good_count, count))
