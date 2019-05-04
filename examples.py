#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# Imports
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

import os
import glob


for file in glob.glob('./examples/*/index.php'):
    html = file.replace('.php', '.html')
    os.system('cd ' + os.path.dirname(file) + ' && php ' + os.path.basename(file) + ' > ' + os.path.basename(html))

    print('Generating ' + html + '.. done')
