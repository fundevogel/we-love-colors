#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# Imports
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

import re


##
# Applies a natural sort order to dictionaries inside a given list
# `list` = list holding dictionaries
# `key` = dictionary key to be sorted by
# See https://stackoverflow.com/a/8940266
##
def natural_sort(list, key='code'):
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]

    sort_key = get_alphanum_key_func(lambda x: x[key])
    list.sort(key=sort_key)
