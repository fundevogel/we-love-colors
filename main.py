#!/usr/bin/env python3

##
# IMPORTS
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

import click

from lib.pantone import Pantone
from lib.ral import RAL
from lib.dulux import Dulux
from lib.copic import Copic
from lib.prismacolor import Prismacolor


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)


class_map = {
    'pantone': Pantone,
    'ral': RAL,
    'dulux': Dulux,
    'copic': Copic,
    'prismacolor': Prismacolor,
}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option('1.0.0-beta.2', '-v', '--version')
def cli():
    pass


@cli.command()
@click.argument('brands', nargs=-1)
def fetch(brands):
    """
    ARGS:
    pantone | ral | dulux | copic | prismacolor
    """
    all_sets = class_map.keys()

    if not brands:
        brands = all_sets

    for brand in brands:
        if brand in all_sets:
            obj = class_map[brand]()

            try:
                obj.fetch_all()

            except AttributeError:
                obj.fetch()

            obj.save()
            obj.create_json()

        else:
            click.echo('"{}" not found. Please provide a valid brand name.'.format(brand))


@cli.command()
@click.argument('brands', nargs=-1)
@click.option('-f', '--output-format', type=click.Choice(['xml', 'gpl', 'acb', 'soc']), help='Color palette format to be generated.')
def process(brands, output_format):
    """
    ARGS:
    pantone | ral | dulux | copic | prismacolor
    """
    all_sets = class_map.keys()

    if not brands:
        brands = all_sets

    for brand in brands:
        if brand in all_sets:
            obj = class_map[brand]()

            if output_format:
                getattr(obj, 'make_' + output_format, None)()

            else:
                obj.make_palettes()

        else:
            click.echo('"{}" not found. Please provide a valid brand name.'.format(brand))


if __name__ == '__main__':
    cli()
