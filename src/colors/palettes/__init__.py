"""
This module is part of the 'we-love-colors' package,
which is released under MIT license.
"""

from .copic import Copic
from .dulux import Dulux
from .pantone import Pantone
from .prismacolor import Prismacolor
from .ral import RAL


PALETTES = {
    "pantone": Pantone,
    "ral": RAL,
    "dulux": Dulux,
    "copic": Copic,
    "prismacolor": Prismacolor,
}

__all__ = [
    # Collection
    "PALETTES",

    # Single palettes
    "Copic",
    "Dulux",
    "Pantone",
    "Prismacolor",
    "RAL",
]
