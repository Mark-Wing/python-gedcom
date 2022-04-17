<p align="center">
  <img src="logo.png">
</p>

<p align="center">
    <a href="https://github.com/mark-wing/python-gedcom/releases" target="_blank"><img src="https://img.shields.io/github/release/mark-wing/python-gedcom.svg" alt="GitHub release"></a>
    <img src="https://img.shields.io/badge/GEDCOM%20format%20version-5.5-yellowgreen.svg" alt="GEDCOM format version 5.5">
    <img src="https://img.shields.io/badge/Python%20versions-3.6%20to%203.10-yellowgreen.svg" alt="Python versions 3.6 to 3.10">
</p>

A Python module for parsing, analyzing, and manipulating GEDCOM files.

GEDCOM files contain ancestry data. The parser is currently supporting the GEDCOM 5.5 format which is detailed at:

https://chronoplexsoftware.com/gedcomvalidator/gedcom/gedcom-5.5.pdf

The python-gedcom includes modules that will complete the following:

* Create a new GEDCOM file based on a person and their descendants.

  * While this is common function of most genealogy programs, the programs do not include the parents of spouses automatically. The python-gedcom module can include them automatically. In fact this problem was the initial driver for the expansion of the python-gedcom.

Future modules in development:

* Create a genealogy book

* Calculated statistics

* Clean GEDCOMs or merge records

## Documentation

Documentation can be found here: https://python-gedcom.readthedocs.io/en/latest/

## Changelog

For the latest changes please have a look at the [`CHANGELOG.md`](CHANGELOG.md) file.

The current development process can be tracked in the [develop branch](https://github.com/Mark-Wing/python-gedcom/tree/develop).

## Common problems

* When you name your script `gedcom.py`, and import the `gedcom` module from this package, running your script won't
  work because Python will try to resolve imports like `gedcom.element.individual` from within your `gedcom.py` but
  not from within the module from this package. Rename your file in this case. ([#26](https://github.com/nickreynke/python-gedcom/issues/26))

### Running tests

1. Run `pipenv install -d` to install normal and dev dependencies
1. Run tests with [tox](https://tox.readthedocs.io/en/latest/index.html) (`pipenv run tox` in your console)
    * For Python 3.6 run `pipenv run tox -e py36` (you need to have Python 3.6 installed)
    * For Python 3.7 run `pipenv run tox -e py37` (you need to have Python 3.7 installed)
    * For Python 3.8 run `pipenv run tox -e py38` (you need to have Python 3.8 installed)
    * For Python 3.9 run `pipenv run tox -e py39` (you need to have Python 3.9 installed)
    * For Python 3.10 run `pipenv run tox -e py310` (you need to have Python 3.10 installed)

### Generating docs

1. Run `pipenv install -d` to install normal and dev dependencies
1. Run `pipenv run pdoc3 --html -o docs/ gedcom --force` to generate docs into the `docs/` directory

> To develop docs run `pipenv run pdoc3 --http localhost:8000 gedcom`
> to watch files and instantly see changes in your browser under http://localhost:8000.

## History

This module was originally based on a GEDCOM parser written by Daniel Zappala at Brigham Young University 
[Copyright (C) 2005].  It was licensed under the GPL v2 and then continued by Mad Price Ball (https://github.com/madprime) in 2012.

The project was taken over by Nicklas Reincke (https://github.com/nickreynke) in 2018.
Together with  Damon Brodie (https://github.com/nomadyow) a lot of changes were made and the parser was optimized.

In 2022, Mark Wing (https://github.com/mark-wing) forked this project and added additional features that support his genealogy projects.

## License

Licensed under the [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)

**Python GEDCOM Parser**
<br>Copyright (C) 2022 Mark Wing (mark at markwing.net)
<br>Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
<br>Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
<br>Copyright (C) 2016 Andreas Oberritter
<br>Copyright (C) 2012 Madeleine Price Ball
<br>Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
<br>Copyright (C) 2005 Brigham Young University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
