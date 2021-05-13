#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Imports
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

from os import system
from os.path import basename, dirname
from glob import glob


for file in glob('./examples/*/index.php'):
    html = file.replace('.php', '.html')
    system('cd ' + dirname(file) + ' && php ' + basename(file) + ' > ' + basename(html))

    print('Generating ' + html + ' .. done')
