# coding: utf-8
import csv
import json

hotels = {}

with open('data/hotels.csv', 'r') as f:
    for row in csv.DictReader(f):
        name = row['Pavadinimas']
        address = row['Veiklos vykdymo vieta']
        del row['Pavadinimas']
        del row['Veiklos vykdymo vieta']
        hotel = {
            'name': name,
            'address': address,
            'info': row,
            'halls': [],
        }
        hotels[name] = hotel

with open('data/halls.csv', 'r') as f:
    for row in csv.DictReader(f):
        hotel_name = row['Viešbutis']
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

        hotel = hotels[hotel_name]
        hotel['halls'].append({
            'name': name,
            'configurations': configs,
            'hardware': hardware,
        })

with open('site/js/data.js', 'w') as f:
    f.write('hotels = (')
    f.write(json.dumps(list(hotels.values()), indent=4))
    f.write(');')

