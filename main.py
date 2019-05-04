#!/usr/bin/env python3

##
# IMPORTS
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

from lib.pantone import Pantone
from lib.ral import Ral
from lib.dulux import Dulux
from lib.copic import Copic
from lib.prismacolor import Prismacolor

pantone = Pantone()
pantone.fetch('graphic-design', 1, 32)
pantone.fetch('fashion-design', 1, 14)
pantone.fetch('product-design', 1, 10)
pantone.save()
pantone.create_json()

ral = Ral()
ral.fetch('classic')
ral.fetch('design')
ral.fetch('effect')
ral.fetch('plastics')
ral.save()
ral.create_json()

dulux = Dulux()
dulux.fetch('dulux')
dulux.save()
dulux.create_json()

copic = Copic()
copic.fetch('copic')
copic.save()
copic.create_json()

prismacolor = Prismacolor()
prismacolor.fetch('premier')
prismacolor.save()
prismacolor.create_json()
