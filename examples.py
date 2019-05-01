#!/usr/bin/env python

import glob, os

for file in glob.glob('./examples/*/index.php'):
    html = file.replace('.php', '.html')
    os.system('cd ' + os.path.dirname(file) + ' && php ' + os.path.basename(file) + ' > ' + os.path.basename(html))
