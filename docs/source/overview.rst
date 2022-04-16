========
Overview
========

The python-gedcom module parses a GEDCOM file and creates a model for accessing its elements.  To understand 
how this works, it is best to first understand the GEDCOM file format.  Each line in the GEDCOM file 
follows this format:

	[level] [pointer] [tag] [value]

An example is::

	0 @I19@ INDI
	1 NAME Grace /Goodhue/
	1 SEX F
	1 BIRT
	2 DATE 3 JAN 1879
	2 PLAC Vermont, USA
	3 MAP
	4 LATI N43.8726
	4 LONG W71.55
	1 DEAT
	2 DATE 8 JUL 1957
	1 FAMS @F8@
	1 FAMC @F5@

The level and tag fields are required.  The level ranges from 0 to 4 and reflects the records relationship 
in the hierarchy.  Any record with a 0 is at the top of the hierarchy and will be referred to as the 
top-level element.  Any record with at level 1 is a child element of the last top-level element.  Any record 
at level 2 is a child of the last level 1 and so on.  If we added indentations to reflect the hierarchy of 
the data, it would look like::

	0 @I19@ INDI
	  1 NAME Grace /Goodhue/
	  1 SEX F
	  1 BIRT
	    2 DATE 3 JAN 1879
 	    2 PLAC Vermont, USA
	      3 MAP
	        4 LATI N43.8726
	        4 LONG W71.55
	  1 DEAT
	    2 DATE 8 JUL 1957
	  1 FAMS @F8@
	  1 FAMC @F5@
	
The pointer and value are optional fields.  The pointer connects records.  For example, the pointer for an 
individual may be used for the record that creates a family group.  The pointer is required for most 
top-level elements and not used by any other level.   The tag is a capitalized three or four-letter word 
that indicates the type of record.  The value field includes the data related to the field.  For example, if 
the tag is for a line is “DATE”, you would expect it to be followed by a date.  If the tag is “FAMS”, you 
would expect in the value field a pointer to another top-level element.  Even though this is a pointer for 
another element, it is in the value field position and therefore is a value.

As the parser works through the file, it creates an object for each line using either the class 
``gedcom.element.Element`` or a class that extends ``gedcom.element.Element``.  For ease of explanation, we 
will initially assume the parser only creates Elements.  Each Element includes the level and tag.  When 
applicable, it includes the pointer, value and a list of child Elements.  If the new Element is a top-level 
element, the parser appends it to the list of top-level elements.  Otherwise, it is appends to the list of 
child Elements maintained by its parent Element.  

The ``gedcom.element.Element`` class uses the following methods to allow access to data for each Element:

* ``get_level()``
* ``get_tag()``
* ``get_pointer()``
* ``get_value()``
* ``get_child_elements()``
* ``get_child_value_by_tag(tag)``

With only these methods, you can access all of the data contained in the GEDCOM file.  This script goes 
through the list of top-level elements and displays their tag and pointer.::
	
	for element in parser.get_root_child_elements():
	    print("First Level", element.get_tag(), element.get_pointer())
    		
We can extend the script to include the tag and value of the second level elements.::

    for element in parser.get_root_child_elements():
        print("First Level", element.get_tag(), element.get_pointer())
        for child in element.get_child_elements():
            print("Second Level", child.get_tag(), child.get_value())

What if we only want names?  Names are second level elements for individuals.  We can iterate through each 
top-level element and search for child elements with the tag “NAME”.::

    for element in parser.get_root_child_elements():
        if element.get_tag() == gedcom.tags.GEDCOM_TAG_INDIVIDUAL:
            for child in element.get_child_elements():
                if child.get_tag() == gedcom.tags.GEDCOM_TAG_NAME:
                    print(child.get_value())

Note: The ``class gedcom.tags`` includes constants for many tags, but not all.

Another options is we can use the ``get_child_value_by_tag(tag)`` method to get names::

    for element in parser.get_root_child_elements():
        if element.get_tag() == gedcom.tags.GEDCOM_TAG_INDIVIDUAL:
            print(element.get_child_value_by_tag(gedcom.tags.GEDCOM_TAG_NAME))
			
Initially we assumed the parser only creates Elements.  The python-gedcom module includes classes that extend 
``gedcom.element.Elements``.  When creating new Elements, the parser uses the tag to determine if the new class 
is an Element or one of the extended class.   The parser uses extended classes for the following tags:

.. table::
   :widths: auto

   ====  ===========  ================================
   Tag   Description  Extended Class
   ====  ===========  ================================
   INDI  Individual   ``gedcom.element.IndividualElement``
   FAM   Family       ``gedcom.element.FamilyElement``
   OBJE  Object       ``gedcom.element.ObjectElement``
   SOUR  Source       ``gedcom.element.SourceElement``
   REPO  Repository   ``gedcom.element.RepositoryElement``
   ====  ===========  ================================
   
Each of the extended classes offers methods specific to the type of record.  For example, 
``element.element.IndividualElement`` includes the method ``get_name_data()``.  The following 
script displays a list of individuals in the GEDCOM.::

    for element in parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            given_name, surname, suffix, sources = element.get_name_data()
            print(given_name, surname, suffix)

The ``get_name_data()`` method parses the value field into a tuple including the given name, surname and 
suffix. If the code used the ``get_child_value_by_tag(tag)``, it would need to separate the names.

While some methods in the extended classes offer additional data processing, many are just wrappers for the 
``get_child_value_by_tag(tag)`` method.  For example, this is the method for ``get_address()`` in 
``RespositoryElement``.::

    def get_address(self):
        return self.get_child_value_by_tag(gedcom.tags.GEDCOM_TAG_ADDRESS)

The only benefit the get_address() method offers is it makes the code more readable.  This is the case for 
many of the methods in the extended classes.

Sometimes the data you need is not available in the extended classes.  For example, while the 
``FamilyElement`` class includes the pointers for the family members, you need to access each family members’  
``IndividualElement`` to get additional data.  There are methods in the parser that make these connections.  
For example, the following code displays the spouses for an individual.::
 
    for spouse in parser.get_spouses(individual):
        given_name, surname = spouse.get_name()
        print(given_name, surname)
