"""Functions for repeated regex replacement.
"""

import re


def multisub_all_sequential(string, re_repl_pairs):
    """Replaces all matches of every matching regex with its repl, in
    the given order.

    >>> multisub_all_sequential('abbc', (('a', '1b'), ('b', '2')))
    '1222c'
    """
    for regex, repl in re_repl_pairs:
        string = re.sub(regex, repl, string)
    return string




def multisub_one(string, re_repl_pairs):
    """Substitutes the first matching regex.

    >>> multisub_one('abbc', (('a', '1b'), ('b', '2')))
    '1bbbc'
    """
    for regex, repl in re_repl_pairs:
        new_string = re.sub(regex, repl, string)
        if new_string != string:
            return new_string
    return string
