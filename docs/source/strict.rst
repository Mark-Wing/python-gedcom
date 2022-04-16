==============
Strict Parsing
==============

Large sites like Ancestry and MyHeritage (among others) don't always produce perfectly formatted GEDCOM files.
If you encounter errors in parsing, you might consider disabling strict parsing which is enabled by default:

.. code-block:: python

	from gedcom.parser import Parser
	
	# Path to your ".ged" file
	file_path = ''
	
	# Name of your ".ged" file
	file_name = ''
	
	gedcom_parser = Parser()
	gedcom_parser.parse_file(file_path + file_name, False) # Disable strict parsing

Disabling strict parsing will allow the parser to gracefully handle the following quirks:

* Multi-line fields that don't use `CONC` or `CONT`
* Handle the last line not ending in a CRLF (``\r\n``)
