import click

from .palettes import PALETTES


# Add shorthand to 'help' parameter
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option("1.1.0", "-v", "--version")
def cli():
    pass


@cli.command()
@click.argument("brands", nargs=-1)
def fetch(brands):
    """
    ARGS:
    pantone | ral | dulux | copic | prismacolor
    """

    all_sets = PALETTES.keys()

    if not brands:
        brands = all_sets

    for brand in brands:
        if brand in all_sets:
            obj = PALETTES[brand]()

            try:
                obj.fetch_all()

            except AttributeError:
                obj.fetch()

            obj.save()
            obj.create_json()

        else:
            click.echo(f'"{brand}" not found. Please provide a valid brand name.')


@cli.command()
@click.argument("brands", nargs=-1)
@click.option(
    "-f",
    "--output-format",
    type=click.Choice(["xml", "gpl", "acb", "soc"]),
    help="Color palette format to be generated.",
)
def process(brands, output_format):
    """
    ARGS:
    pantone | ral | dulux | copic | prismacolor
    """

    all_sets = PALETTES.keys()

    if not brands:
        brands = all_sets

    for brand in brands:
        if brand in all_sets:
            obj = PALETTES[brand]()

            if output_format:
                getattr(obj, "make_" + output_format, None)()

            else:
                obj.make_palettes()

        else:
            click.echo(
                '"{}" not found. Please provide a valid brand name.'.format(brand)
            )
