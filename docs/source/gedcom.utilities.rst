gedcom.utilities package
========================

Module contents
---------------

The utilities module contains sub-modules that use the GEDCOM Parser to complete useful tasks.  These tasks 
include:

* Splitter

  * Creates a GEDCOM including only specific person, their descendants, their descendant's spouses and the their descendant's spouses' parents.  Many software packages can export descendants and spouses, but do not include in-laws.

* Book

  * Creates a genealogy book for a specific person.
  * Currently in development.

* Scrubber

  * Creates a clean GEDCOM with primary facts, but no alternate facts or sources.
  * Currently in development.

* Statistics

  * Reads the GEDCOM and calculates statistics.
  * Currently in development.


Subpackages
-----------

* :doc:`gedcom.utilities.splitter <gedcom.utilities.splitter>`
