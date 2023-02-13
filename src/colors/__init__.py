"""
This module is part of the 'we-love-colors' package,
which is released under MIT license.
"""

from typing import Dict, List, Optional, Tuple

import click

from .palette import Palette
from .palettes import RAL, Copic, Dulux, Pantone, Prismacolor

# Define available file fornats
FORMATS: List[str] = [
    "acb",
    "gpl",
    "soc",
    "xml",
]


# Map available brands & their classes
PALETTES: Dict[str, Palette] = {
    # "copic": Copic,
    "dulux": Dulux,
    "pantone": Pantone,
    # "prismacolor": Prismacolor,
    # "ral": RAL,
}


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("brands", nargs=-1)
@click.option("-f", "--palette", type=click.Choice(FORMATS), help="Palette format(s).")
@click.version_option("1.1.0", "-v", "--version")
def cli(brands: Optional[Tuple[str]], palette: str):
    """
    BRANDS:
    pantone | ral | dulux | copic | prismacolor
    """

    # Iterate over available brands
    for brand, Brand in PALETTES.items():
        # Check whether single or all brands are selected
        if not brands or brand in brands:
            # Initialize object
            obj = Brand()

            # Retrieve brand colors
            # obj.fetch_colors()

            # Create (selected) palettes
            obj.make_palettes(palette)
