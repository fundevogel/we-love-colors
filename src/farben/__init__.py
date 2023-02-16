"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from typing import Dict, List, Optional, Tuple

import click

from .palette import Palette
from .palettes import NCS, RAL, Copic, Dulux, Pantone, Prismacolor

# Define available file fornats
FORMATS: List[str] = [
    "acb",
    "gpl",
    "soc",
    "xml",
]

# Map available brands & their classes
PALETTES: Dict[str, Palette] = {
    "pantone": Pantone,
    "ral": RAL,
    "dulux": Dulux,
    "copic": Copic,
    "ncs": NCS,
    "prismacolor": Prismacolor,
}


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option("2.0.0-rc", "-v", "--version")
def cli():
    """
    PANTONE®, RAL®, Dulux®, Copic®, NCS® and Prismacolor® color palettes
    for Scribus, GIMP, AutoCAD, Inkscape & LibreOffice.
    """


@cli.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("brands", nargs=-1)
@click.option("-p", "--palette", type=click.Choice(FORMATS), help="Palette format(s).")
def fetch(brands: Optional[Tuple[str]], palette: str):
    """
    BRANDS:
    pantone | ral | dulux | copic | ncs | prismacolor
    """

    # Iterate over available brands
    for brand, Brand in PALETTES.items():
        # Check whether single or all brands are selected
        if not brands or brand in brands:
            # Initialize object
            obj = Brand()

            # Retrieve brand colors
            obj.fetch_colors()

            # Create (selected) palettes
            obj.make_palettes(palette)
