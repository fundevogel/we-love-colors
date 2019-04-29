# We :heart: Pantone®
This library provides an easy way to generate [*color palettes*](https://www.etymonline.com/search?q=Palette):

> In computer graphics, a palette is a finite set of colors.
> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'

.. often referred to as *Swatches* (as branded by [Adobe Inc.](https://www.adobe.com)):

> *Swatches* are named colors, tints, gradients, and patterns.
> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)

.. featuring [PANTONE® colors](https://www.pantone.com) (proprietary color spaces). For now, `we-love-pantone` creates master palettes for use in [Scribus](https://www.scribus.net), an open source desktop publishing program, as well as [GIMP](https://www.gimp.org) and [Inkscape](https://inkscape.org).

## Getting started
.. was never easier. Make sure Python3 is intalled on your system, then simply do:

```bash
python3 fetch.py
python3 process.py
```

## Color samples
If you are looking for a quick way to browse PANTONE® colors, check out the [Pantone Finder](https://github.com/picorana/Pantone_finder) package or [visit their website](https://picorana.github.io/Pantone_finder) to get started. However, there's a quick&dirty preview inside `examples`, which is as easy as opening `index.html`. In case you want to play around with `index.php`, simply `php -S localhost:8000` and enter the world of PANTONE® colors by clicking on a tile to save its hex value to your clipboard - brought to you by [clipboard.js](https://github.com/zenorocha/clipboard.js).

## Copyright
Whenever mentioned throughout this project, PANTONE® and other [Pantone LLC](https://www.pantone.com) trademarks are the property of Pantone LLC, a division of [X-Rite](https://www.xrite.com), a [Danaher](https://www.danaher.com) company. We assume neither ownership nor intellectual property of any kind - color codes (and names), RGB values & hexadecimals are publically available on [their website](https://www.pantone.com).

## Roadmap
- [x] Generating different JSON first
- [x] Permissions when folder doesn't exist
- [x] Introduce natural sorting for set `graphics-design`
- [ ] Deleting entries after being moved to their respective list (eg subset['C'])
- [ ] Filtering pastels & metallics
