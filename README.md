# We love colors!
This library provides an easy way to generate [*color palettes*](https://www.etymonline.com/search?q=Palette):

> In computer graphics, a palette is a finite set of colors.
> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'

.. often referred to as *Swatches* (as branded by [Adobe Inc.](https://www.adobe.com)):

> *Swatches* are named colors, tints, gradients, and patterns.
> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)

.. featuring [PANTONE®](https://www.pantone.com), [RAL®](https://www.ral-farben.de) and [Dulux®](https://www.dulux.com.au) colors (proprietary color spaces). For now, `we-love-colors` creates master palettes for use in [Scribus](https://www.scribus.net), an open source desktop publishing program, as well as [GIMP](https://www.gimp.org) and [Inkscape](https://inkscape.org).

## Getting started
.. was never easier. Make sure Python3 is intalled on your system, then simply do:

```bash
python3 fetch.py # or any other `fetch*` script
python3 process.py
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
- [ ] Making use of CLI arguments
- [x] Automatizing example generation
- [ ] Combining all `fetch` scripts
