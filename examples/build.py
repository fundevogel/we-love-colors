"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

import glob
import os

for file in glob.glob("*/index.php"):
    html = file.replace(".php", ".html")
    os.system(
        "cd "
        + os.path.dirname(file)
        + " && php "
        + os.path.basename(file)
        + " > "
        + os.path.basename(html)
    )

    print("Generating " + html + " .. done")
