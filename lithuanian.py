# -*- coding: utf-8 -*-
"""Language related functions.
"""

import re
import itertools


def multisub_all_separate(string, re_repl_pairs):
    """Returns a set of all the strings that can be created by
    replacing the given regexes with their corresponding replacements
    in the given string.

    >>> r = multisub_all_separate('abbc', (('a', '1b'), ('b', '2')))
    >>> r == set(['1bbbc', 'a22c'])
    True
    """
    r = set()
    for regex, repl in re_repl_pairs:
        new_string = re.sub(regex, repl, string)
        if new_string != string:
            r.add(new_string)
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
    words = thing.split(u' ')
    word_variants = [genitive_to_nominative(word) or [word]
                for word in words]
    thing_variants = itertools.product(*word_variants)
    return [' '.join(w for w in variant)
            for variant in thing_variants]


def subvariants(address):
    yield re.sub(ur'\Wm.(\W|$)', r'\1', address)
    yield address


def address_variants(address):
    address = re.sub(ur', .*? (sav|sen|r)\.', '', address)

    try:
        street, rest = address.split(',', 1)
    except ValueError:
        street = ''
        rest = address

    results = set()
    for v in nominative_names(rest):
        for subv in subvariants(v):
            results.add(subv)
    if address in results:
        results.remove(address)

    if street:
        return [address] + list(street + ', ' + r for r in results)
    else:
        return [address] + list(results)
