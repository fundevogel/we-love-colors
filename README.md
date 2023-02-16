# farben
[![License](https://badgen.net/badge/license/MIT/blue)](https://codeberg.org/Fundevogel/farben/src/branch/main/LICENSE) [![PyPI](https://badgen.net/pypi/v/farben)](https://pypi.org/project/farben) [![Build](https://ci.codeberg.org/api/badges/Fundevogel/farben/status.svg)](https://codeberg.org/Fundevogel/farben/issues)

This library provides an easy way to generate **color palettes**:

> In computer graphics, a palette is a finite set of colors.
> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'

.. often referred to as **Swatches** (as branded by [Adobe Inc.](https://www.adobe.com)):

> *Swatches* are named colors, tints, gradients, and patterns.
> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)

.. featuring the following (proprietary) color spaces:

- [PANTONE®](https://www.pantone.com)
- [RAL®](https://www.ral-farben.de)
- [Dulux®](https://www.dulux.com.au)
- [Copic®](https://www.copicmarker.com)
- [NCS®](https://ncscolour.com)
- [Prismacolor®](https://www.prismacolor.com)

For now, `farben` creates master palettes for use in

- [Scribus](https://www.scribus.net) (XML)
- [GIMP](https://www.gimp.org) (GPL)
- [AutoCAD](https://www.autodesk.com/products/autocad) (ACB)
- [Inkscape](https://inkscape.org) (GPL)
- [LibreOffice](https://www.libreoffice.org) (SOC)


## Installation

It's available from [PyPi](https://pypi.org/project/farben):

```bash
# Using 'pip'
pip install farben

# Using 'poetry'
poetry add farben
```


## Getting started

Using this library is straightforward  - otherwise, `--help` is your friend:

```text
$ farben fetch --help
Usage: farben [OPTIONS] COMMAND [ARGS]...

  PANTONE®, RAL®, Dulux®, Copic®, NCS® and Prismacolor® color palettes for
  Scribus, GIMP, AutoCAD, Inkscape & LibreOffice.

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  fetch  BRANDS: pantone | ral | dulux | copic | ncs | prismacolor
```

Using its `fetch` command is fairly easy, like that:

```bash
# Example 1
# - all brands
# - all palettes
$ farben fetch

# Example 2
# - all brands
# - only specific palette(s)
$ farben fetch -p gpl
$ farben fetch -p gpl -p acb

# Example 3
# - only specific brand(s)
$ farben fetch copic
$ farben fetch copic dulux
```

.. you get the idea!


## FAQ

**Q: But where do all those files go?**
**A:** That depends, ..
- .. `.xml` files may be loaded individually with `Edit - Colours & Fills - Solid Colours - Import` (Scribus)
- .. `.soc` files belong here:
  - `~\AppData\Roaming\libreoffice\3\user` (Windows + PowerShell, otherwise `%userprofile%`)
  - `~/Library/Application Support/libreoffice/4/user/config` (Mac)
  - `~/.config/libreoffice/4/user/config` (Linux)
- .. installing `.gpl` files boils down to:
  - moving them to any path specified in `Edit - Preferences - Folders - Palettes` (GIMP)
  - moving them to `palettes` under directory specified in `Edit - Preferences - System - User Config` (Inkscape)
- .. installing `.acb` files is [pretty straightforward](https://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/AutoCAD-Core/files/GUID-17E00AB3-3065-4F1B-A1C3-C4963396D2CB-htm.html)


## Color samples

If you are looking for a quick way to browse PANTONE® colors, check out the [Pantone Finder](https://github.com/picorana/Pantone_finder) package or [visit their website](https://picorana.github.io/Pantone_finder) to get started.

Once you retrieved color palettes, you can

- view them using PHP like this: `cd examples/{brand} && php -S localhost:8000`
- view static HTML page like this: `cd examples && python build.py`

When clicking on a color tile, its hex value is copied to your clipboard (powered by [clipboard.js](https://github.com/zenorocha/clipboard.js)).


## Copyright

Whenever mentioned throughout this project, PANTONE® and related trademarks are the property of [Pantone LLC](https://www.pantone.com), a division of [X-Rite](https://www.xrite.com), a [Danaher](https://www.danaher.com) company.

The same applies to ..
- RAL® and related trademarks of [RAL gGmbH](https://www.ral-farben.de) (non-profit LLC) and [RAL Deutsches Institut für Gütesicherung und Kennzeichnung e. V.](https://www.ral.de)
- Dulux® and related trademarks of [AkzoNobel N.V.](https://www.akzonobel.com) (worldwide) and [DuluxGroup](https://www.dulux.com.au) (Australia & New Zealand)
- Copic® and related trademarks of [Too Marker Corporation](https://www.toomarker.co.jp/en)
- Natural Colour System® and related trademarks of [NCS Colour AB](https://ncscolour.com)
- Prismacolor® and related trademarks of [Berol Corporation](http://www.berol.co.uk), owned by [Sanford L.P.](http://www.sanfordb2b.com), a [Newell Brands](https://www.newellbrands.com) company.

We assume neither ownership nor intellectual property of any kind - color codes (and names), sRGB and/or hexadecimal values are publically available on the internet.


## Similar projects

- For Scribus, there's also the (currently unmaintained) package [`SwatchBooker`](http://www.selapa.net/swatchbooker)


**Happy coding!**


:copyright: Fundevogel Kinder- und Jugendbuchhandlung
