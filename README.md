# We love colors!
This library provides an easy way to generate [*color palettes*](https://www.etymonline.com/search?q=Palette):

> In computer graphics, a palette is a finite set of colors.
> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'

.. often referred to as *Swatches* (as branded by [Adobe Inc.](https://www.adobe.com)):

> *Swatches* are named colors, tints, gradients, and patterns.
> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)

.. featuring [PANTONE®](https://www.pantone.com), [RAL®](https://www.ral-farben.de), [Dulux®](https://www.dulux.com.au) as well as [Copic®](https://www.copicmarker.com) and [Prismacolor®](https://www.prismacolor.com) (proprietary color spaces). For now, `we-love-colors` creates master palettes for use in [Scribus](https://www.scribus.net), an open source desktop publishing program, as well as [GIMP](https://www.gimp.org) and [Inkscape](https://inkscape.org).

## Getting started
Depending on your setup you might prefer a ..

### Local installation via `virtualenv`
Running `setup.sh` will install all dependencies inside a virtual environment, ready for action.

### Global installation via `requirements.txt`
It's as easy as `pip install -r requirements.txt`, but you might want to make sure that Python v3 is installed on your system.

## Usage
Fetching color sets and processing them is really straightforward - for everything else, there's  `--help`:

```bash
$ python main.py
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  fetch    ARGS: pantone | ral | dulux | copic | prismacolor
  process  ARGS: pantone | ral | dulux | copic | prismacolor


# Example 1 - Gotta fetch 'em `--all`:
$ python main.py fetch --all && python main.py process --all

# Example 2 - Fetching two sets & processing them:
$ python main.py fetch copic dulux && python main.py process copic dulux # or simply `--all`
```

## Color samples
If you are looking for a quick way to browse PANTONE® colors, check out the [Pantone Finder](https://github.com/picorana/Pantone_finder) package or [visit their website](https://picorana.github.io/Pantone_finder) to get started.

For all included colors, there are preview files, to be found in the `examples` folder: Open up `index.html`, generated with `examples.py` (for its PHP version, just `php -S localhost:8000`).

When clicking a color tile, its hex value is copied to your clipboard - brought to you by [clipboard.js](https://github.com/zenorocha/clipboard.js).

## Copyright
Whenever mentioned throughout this project, PANTONE® and related trademarks are the property of [Pantone LLC](https://www.pantone.com), a division of [X-Rite](https://www.xrite.com), a [Danaher](https://www.danaher.com) company.

The same applies to ..
- RAL® and related trademarks of [RAL gGmbH](https://www.ral-farben.de) (non-profit LLC) and [RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V.](https://www.ral.de)
- Dulux® and related trademarks of [AkzoNobel N.V.](https://www.akzonobel.com) (worldwide) and [DuluxGroup](https://www.dulux.com.au) (Australia & New Zealand)
- Copic® and related trademarks of [Too Marker Corporation](https://www.toomarker.co.jp/en)
- Prismacolor® and related trademarks of [Berol Corporation](http://www.berol.co.uk), owned by [Sanford L.P.](http://www.sanfordb2b.com), a [Newell Brands](https://www.newellbrands.com) company.

We assume neither ownership nor intellectual property of any kind - color codes (and names), sRGB and/or hexadecimal values are publically available on (one of) their respective websites.

## Similar projects
- For Scribus, there's also the (currently unmaintained) package [`SwatchBooker`](http://www.selapa.net/swatchbooker)

## Roadmap
- [x] Generating different JSON first
- [x] Permissions when folder doesn't exist
- [x] Introduce natural sorting for set `graphics-design`
- [x] ~~Deleting~~ Skipping entries after being moved to their respective list
- [x] Filtering neons, pastels & metallics
- [x] Adding copyright notice for RAL®/Dulux® (XML + GPL) + fallback option
- [x] Adding examples for all color palettes
- [x] Making use of CLI arguments
- [x] Automatizing example generation
- [x] Combining all `fetch` scripts
- [x] Cleaning up examples (merge CSS, remove RGB2hex & PHP error settings)
