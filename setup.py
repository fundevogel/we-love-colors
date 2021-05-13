# ~*~ coding=utf-8 ~*~

import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


VERSION = '1.0.0'


def long_description():
    readme_file = join(dirname(abspath(__file__)), 'README.md')

    with io.open(readme_file, encoding='utf8') as file:
        return file.read()


setup(
    name='we-love-colors',
    description='PANTONE®, RAL®, Dulux®, Copic® and Prismacolor® color palettes for Scribus, GIMP & Inkscape, the Python way',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    version=VERSION,
    license='MIT',
    author='Martin Folkers',
    author_email='hello@twobrain.io',
    maintainer='Fundevogel',
    maintainer_email='maschinenraum@fundevogel.de',
    url='https://github.com/Fundevogel/we-love-colors',
    project_urls={
        "Source code": "https://github.com/Fundevogel/we-love-colors",
        "Issues": "https://github.com/Fundevogel/we-love-colors/issues",
    },
    packages=find_packages(),
    install_requires=[
        'bs4',
        'click',
        'lxml',
        'pillow',
    ],
    entry_points='''
        [console_scripts]
        colors=we_love_colors.cli:cli
    ''',
    python_requires='>=3.5',
)
