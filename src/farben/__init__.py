"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from typing import Dict, List, Optional, Tuple

import click

from .palettes import NCS, RAL, Copic, Dulux, Pantone, Prismacolor


fetch_args = {
    "type": click.Choice(["acb", "gpl", "soc", "xml"]),
    "multiple": True,
    "help": "Palette format(s).",
}


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option("2.0.0", "-v", "--version")
def cli():
    """
    PANTONE®, RAL®, Dulux®, Copic®, NCS® and Prismacolor® color palettes
    for Scribus, GIMP, AutoCAD, Inkscape & LibreOffice.
    """


@cli.command()
@click.argument("brands", nargs=-1)
@click.option("-p", "--palette", **fetch_args)
def fetch(brands: Optional[Tuple[str]], palette: Tuple[str]):
    """
    BRANDS:
    pantone | ral | dulux | copic | ncs | prismacolor
    """

    # Map available brands & their classes
    all_brands = {
        "pantone": Pantone,
        "ral": RAL,
        "dulux": Dulux,
        "copic": Copic,
        "ncs": NCS,
        "prismacolor": Prismacolor,
    }

    # Iterate over available brands
    for brand, Brand in all_brands.items():
        # Check whether single or all brands are selected
        if not brands or brand in brands:
            # Initialize object
            obj = Brand()

            # Retrieve brand colors
            obj.fetch_colors()

            # Create (selected) palettes
            obj.make_palettes(palette)
