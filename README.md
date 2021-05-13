# We love colors!
This library provides an easy way to generate [*color palettes*](https://www.etymonline.com/search?q=Palette):

> In computer graphics, a palette is a finite set of colors.
> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'

.. often referred to as *Swatches* (as branded by [Adobe Inc.](https://www.adobe.com)):

> *Swatches* are named colors, tints, gradients, and patterns.
> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)

.. featuring the following (proprietary) color spaces:
- [PANTONE®](https://www.pantone.com)
- [RAL®](https://www.ral-farben.de)
- [Dulux®](https://www.dulux.com.au)
- [Copic®](https://www.copicmarker.com)
- [Prismacolor®](https://www.prismacolor.com)

For now, `we-love-colors` creates master palettes for use in
- [Scribus](https://www.scribus.net) (XML)
- [GIMP](https://www.gimp.org) and [Inkscape](https://inkscape.org) (GPL)
- [AutoCAD](https://www.autodesk.com/products/autocad) (ACB)
- [LibreOffice](https://www.libreoffice.org) (SOC)

## Getting started
Depending on your setup you might prefer a ..

### Local installation via `virtualenv`
Running `setup.sh` will install all dependencies inside a virtual environment, ready for action.

### Global installation via `requirements.txt`
It's as easy as `pip install -r requirements.txt`, but you might want to make sure that Python v3 is installed on your system.

## Usage
Fetching color sets and processing them is really straightforward - for everything else, there's  `--help`:

```bash
$ colors
Usage: colors [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  fetch    ARGS: pantone | ral | dulux | copic | prismacolor
  process  ARGS: pantone | ral | dulux | copic | prismacolor
```

Using its commands `fetch` and `process` is fairly easy, like that:

```bash
# Example 1 - Gotta fetch 'em `--all`:
$ colors fetch --all && colors process

# Example 2 - Fetching specific sets & processing them:
$ colors fetch copic dulux && colors process copic dulux
```

### FAQ
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


**Happy coding!**


:copyright: Fundevogel Kinder- und Jugendbuchhandlung
