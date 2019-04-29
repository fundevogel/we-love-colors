# We :heart: Pantone®
This library provides an easy way to generate [*color palettes*](https://www.etymonline.com/search?q=Palette):

> In computer graphics, a palette is a finite set of colors.
> — Wikipedia article '[Palette (Computing)](https://en.wikipedia.org/wiki/Palette_(computing))'

.. often referred to as *Swatches* (as branded by [Adobe Inc.](https://www.adobe.com)):

> *Swatches* are named colors, tints, gradients, and patterns.
> — [Adobe Illustrator](https://helpx.adobe.com/illustrator/using/using-creating-swatches.html)

.. featuring [PANTONE® colors](https://www.pantone.com) (proprietary color spaces). For now, `python3 fetch.py` & `php process.php` create master palettes for use in [Scribus](https://www.scribus.net), an open source desktop publishing program.

## Credits
Inspired by [Pantone Finder](https://github.com/picorana/Pantone_finder), whose (slightly modified) python script is used to aggregate information on each color inside `pantone.json`.

## Copyright
Whenever mentioned throughout this project, PANTONE® and other [Pantone LLC](https://www.pantone.com) trademarks are the property of Pantone LLC, a division of [X-Rite](https://www.xrite.com), a [Danaher](https://www.danaher.com) company. We assume neither ownership nor intellectual property of any kind - color codes (and names), RGB values & hexadecimals are publically available on [their website](https://www.pantone.com).

TODO:
- [ ] Permissions when folder doesn't exist
- [x] Generating different JSON first
