"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from .copic import Copic
from .dulux import Dulux
from .hks import HKS
from .ncs import NCS
from .pantone import Pantone
from .prismacolor import Prismacolor
from .ral import RAL

__all__ = [
    "Copic",
    "Dulux",
    "HKS",
    "NCS",
    "Pantone",
    "Prismacolor",
    "RAL",
]
