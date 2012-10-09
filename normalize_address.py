# coding: utf-8

import re
import itertools


def multisub_all_separate(string, re_repl_pairs):
    """Returns a set of all the strings that can be created by
    replacing the given regexes with their corresponding replacements
    in the given string.

    >>> r = multisub_all_separate('abbc', (('a', '1b'), ('b', '2')))
    >>> set(r) == set(['1bbbc', 'a22c'])
    True
    """
    r = list()
    for regex, repl in re_repl_pairs:
        new_string = re.sub(regex, repl, string)
        if new_string != string:
            r.append(new_string)
    return r


def genitive_to_nominative(word):
    u"""Find possible conversions of a lithuanian word from genitive to
    the nominative case as a set.

    Of course, each word has only one such conversion, but it's
    complicated to determine it, so we just match the words' endings
    and return all possible variants. This is good enough for indexing
    various ways to spell city names for search.

    >>> u'raudonieji' in genitive_to_nominative(u'raudonųjų')
    True
    >>> u'raudonasis' in genitive_to_nominative(u'raudonojo')
    True
    >>> u'Vilnius' in genitive_to_nominative(u'Vilniaus')
    True
    >>> u'Pakonys' in genitive_to_nominative(u'Pakonių')
    True
    >>> u'Gedvydžiai' in genitive_to_nominative(u'Gedvydžių')
    True
    >>> u'Bajorai' in genitive_to_nominative(u'Bajorų')
    True
    """
    c = ur'([bdfghjklmnprsštvwzž])'     # one consonant
    endw = ur'(\W|$)'
    return multisub_all_separate(word, (
        (c + ur'ųjų' + endw, ur'\1ieji\2'),
        (c + ur'ojo' + endw, ur'\1asis\2'),
        (c + ur'osios' + endw, ur'\1oji\2'),

        (c + ur'iaus' + endw, ur'\1ius\2'),
        (c + ur'ių' + endw, ur'\1ys\2'),
        (c + ur'ių' + endw, ur'\1iai\2'),
        (c + ur'ių' + endw, ur'\1ės\2'),
        (c + ur'ų' + endw, ur'\1ai\2'),
        (c + ur'ų' + endw, ur'\1os\2'),

        (c + ur'io' + endw, ur'\1is\2'),
        (c + ur'io' + endw, ur'\1ys\2'),
        (c + ur'o' + endw, ur'\1as\2'),
        (c + ur'os' + endw, ur'\1a\2'),

        (c + ur'ės' + endw, ur'\1ė\2'),
    ))


def nominative_names(thing):
    u"""Turn a genitive title into a list of possible nominative ones.

    Also, removes any lowercase words from the title, to remove
    specifiers like 'miestas' in 'Vilniaus miestas', etc.

    Only suitable for search indexes, not for display, because only
    one of the nominative variants is correct.

    >>> u'Gedvydžiai' in nominative_names(u'Gedvydžių kaimas')
    True
    >>> u'Vilnius' in nominative_names(u'Vilniaus miestas')
    True
    >>> u'Pakonys I' in nominative_names(u'Pakonių I')
    True
    >>> u'Raudonieji Dobilai' in nominative_names(u'Raudonųjų Dobilų')
    True
    """
    words = thing.split(u' ')
    word_variants = [genitive_to_nominative(word) or [word]
                for word in words]
    thing_variants = itertools.product(*word_variants)
    return [' '.join(w for w in variant if not w.islower())
            for variant in thing_variants]


class Field(object):
    ordinal = -1
    replacements = ()

    def __init__(self, field, all_fields):
        self.field = field
        self.all_fields = all_fields
        self.variants = list(self.process()) + [self.field, None]

    def __cmp__(a, b):
        return cmp(a.ordinal, b.ordinal)

    def __unicode__(self):
        return u'<{}: {}>'.format(
            self.__class__.__name__,
            self.variants,
        )

    # default implementation replaces one of the patterns
    def process(self):
        for pattern, repl in self.replacements:
            result, count = re.subn(pattern, repl, self.field)
            if count:
                yield result
                break
        else:
            yield self.field


class Remove(Field):
    def __init__(self, field, all_fields):
        self.variants = [None]


class Street(Field):
    ordinal = 0

    replacements = (
        (ur'\bg\.(\W|$)', ur'gatvė\1'),
        (ur'\bpr\.(\W|$)', ur'prospektas\1'),
        (ur'\bal?\.(\W|$)', ur'alėja\1'),
    )

    def process(self):
        self.field = re.sub(ur'(\d)-\d+', ur'\1', self.field)
        self.field = re.sub(ur'/.*', u'', self.field)
        return super(Street, self).process()


class Municipality(Field):
    ordinal = 10

    replacements = (
        (ur'\bm\.\ssav\.(\W|$)', ur'miesto savivaldybė\1'),
        (ur'\br\.\ssav\.(\W|$)', ur'rajono savivaldybė\1'),
        (ur'\br\.(\W|$)', ur'rajono savivaldybė\1'),
    )


class Nominative(Field):
    ordinal = 3

    replacements = (
        (ur'\bm\.(\W|$)', ur'miestas\1'),
        (ur'\bkm?\.(\W|$)', ur'kaimas\1'),
    )

    def process(self):
        return itertools.chain(
            super(Nominative, self).process(),
            nominative_names(self.field),
        )


class City(Field):
    ordinal = 3
    
    def process(self):
        return []


class Unknown(Field):
    ordinal = 0

    def process(self):
        return []


CITIES = (
    u'Akmenė',
    u'Alytus',
    u'Anykščiai',
    u'Ariogala',
    u'Baltoji Vokė',
    u'Birštonas',
    u'Biržai',
    u'Daugai',
    u'Druskininkai',
    u'Dūkštas',
    u'Dusetos',
    u'Eišiškės',
    u'Elektrėnai',
    u'Ežerėlis',
    u'Gargždai',
    u'Garliava',
    u'Gelgaudiškis',
    u'Grigiškės',
    u'Ignalina',
    u'Jieznas',
    u'Jonava',
    u'Joniškėlis',
    u'Joniškis',
    u'Jurbarkas',
    u'Kaišiadorys',
    u'Kalvarija',
    u'Kaunas',
    u'Kavarskas',
    u'Kazlų Rūda',
    u'Kėdainiai',
    u'Kelmė',
    u'Kybartai',
    u'Klaipėda',
    u'Kretinga',
    u'Kudirkos Naumiestis',
    u'Kupiškis',
    u'Kuršėnai',
    u'Lazdijai',
    u'Lentvaris',
    u'Linkuva',
    u'Marijampolė',
    u'Mažeikiai',
    u'Molėtai',
    u'Naujoji Akmenė',
    u'Nemenčinė',
    u'Neringa',
    u'Obeliai',
    u'Pabradė',
    u'Pagėgiai',
    u'Pakruojis',
    u'Palanga',
    u'Pandėlys',
    u'Tauragė',
    u'Panevėžys',
    u'Pasvalys',
    u'Plungė',
    u'Priekulė',
    u'Prienai',
    u'Radviliškis',
    u'Ramygala',
    u'Raseiniai',
    u'Rietavas',
    u'Rokiškis',
    u'Rumšiškės',
    u'Rūdiškės',
    u'Salantai',
    u'Seda',
    u'Simnas',
    u'Skaudvilė',
    u'Skuodas',
    u'Šakiai',
    u'Šalčininkai',
    u'Šeduva',
    u'Šiauliai',
    u'Šilalė',
    u'Šilutė',
    u'Širvintos',
    u'Švenčionėliai',
    u'Švenčionys',
    u'Tauragė',
    u'Telšiai',
    u'Tytuvėnai',
    u'Trakai',
    u'Troškūnai',
    u'Ukmergė',
    u'Utena',
    u'Užventis',
    u'Vabalninkas',
    u'Varėna',
    u'Varniai',
    u'Veisiejai',
    u'Venta',
    u'Viekšniai',
    u'Vievis',
    u'Vilkaviškis',
    u'Vilkija',
    u'Vilnius',
    u'Virbalis',
    u'Visaginas',
    u'Zarasai',
    u'Žagarė',
    u'Žiežmariai',
)

CITIES_REGEXP = ur'\b(' + ur'|'.join(CITIES) + ur')(\W|$)'

PROCESSORS = (
    (ur'\bg\.(\W|$)', Street),
    (ur'\bpr\.(\W|$)', Street),
    (ur'\bsav\.(\W|$)', Municipality),
    (ur'\br\.(\W|$)', Municipality),
    (ur'\bkm?\.(\W|$)', Nominative),
    (ur'\bm\.(\W|$)', Nominative),
    (ur'\bsen\.(\W|$)', Remove),
    (CITIES_REGEXP, City),
)


def process(f, fields):
    for pattern, kind in PROCESSORS:
        if re.search(pattern, f):
            return kind(f, fields)
    else:
        return Unknown(f, fields)


def join_address(xs):
    return u', '.join(x for x in xs if x)


def normalize_address(address):
    fields = [f.strip() for f in address.split(u',')]
    processed = [process(f, fields) for f in fields]
    processed.sort()
    subvariants = [p.variants for p in processed] + [[u'Lietuva']]
    variants = itertools.product(*subvariants)
    joined = map(join_address, variants)
    return [j for j in joined if j != u'Lietuva'] # remove empty


if __name__ == '__main__':
    import csv
    for x in csv.reader(open('data/hotels.csv', 'r')):
        print x[1]
        variants = normalize_address(x[1].decode('utf-8'))
        for var in variants:
            print '    ', var.encode('utf-8')
