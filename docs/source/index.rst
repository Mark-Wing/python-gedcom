=============
Module gedcom
=============

A Python module for parsing, analyzing, and manipulating GEDCOM files.

GEDCOM files contain ancestry data. The parser is currently supporting the GEDCOM 5.5 format which is detailed at:

https://chronoplexsoftware.com/gedcomvalidator/gedcom/gedcom-5.5.pdf.

History
=======
This module was originally based on a GEDCOM parser written by Daniel Zappala at Brigham Young University 
[Copyright (C) 2005].  It was licensed under the GPL v2 and then continued by Mad Price Ball (https://github.com/madprime) in 2012.

The project was taken over by Nicklas Reincke (https://github.com/nickreynke) in 2018.
Together with  Damon Brodie (https://github.com/nomadyow) a lot of changes were made and the parser was optimized.

In 2022, Mark Wing forked this project and added additional features that support his genealogy projects.

New Features
============
parser.py
---------
Updates to existing methods:

* Added optional ``parent_type`` to ``find_path_to_ancestor``

  * The ``find_path_to_ancestor`` assumed the parent type is "Natural". 
  
  * This is not part of the 5.5 GEDCOM standard and as a result, may not work for some GEDCOMs  

* Added optional ``callback`` method to ``parse_file`` method. 

  * Larger files take a long time to parse. The callback allows the calling program to monitor progress.    

New methods:

* ``find_all_path_to_ancestor``

  * The ``find_path_to_ancestor`` only finds one path.  Sometimes there is more than one.

* ``get_children``
* ``get_family``
* ``get_spouses``
* ``get_marriage_data``

element.py
----------
New methods:

* ``equals``
* ``get_child_value_by_tag``
* ``remove_child_element``

individual.py
-------------
Updates to existing methods:

* Updated ``criteria_match`` to support ``given_name`` in criteria

New methods:

* ``get_birth_date``
* ``get_birth_place``
* ``get_death_date``
* ``get_death_place``
* ``get_first_name``
* ``get_name_data``
* ``get_sources_by_value``
* ``get_sources_by_tag_and_date``
* ``get_sources_by_tag_and_place``
* ``get_vital_data_by_tag``
* ``get_vital_year_by_tag``

Utilities
---------
The python-gedcom includes modules that will complete the following:

* Create a new GEDCOM file based on a person and their descendants.  

  * While this is common function of most genealogy programs, the programs do not include the parents of spouses automatically.  The python-gedcom module can include them automatically.  In fact this problem was the initial driver for the expansion of the python-gedcom.

Future modules in development:

* Create a genealogy book
* Calculated statistics
* Clean GEDCOMs or merge records

Change Log
==========
A complete set of changes can be found at:

https://github.com/Mark-Wing/python-gedcom/blob/master/CHANGELOG.md

License
=======
Copyright (C) 2022 Mark Wing (mark at markwing.net)

Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)

Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)

Copyright (C) 2016 Andreas Oberritter

Copyright (C) 2012 Madeleine Price Ball

Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)

Copyright (C) 2005 Brigham Young University

Navigation
==========
.. toctree::
   :maxdepth: 2

   index
   overview
   strict
   install
   examples
   splitter
   autoapi/index
   support
   

