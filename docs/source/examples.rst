========
Examples
========

Example 1
---------
The first example finds all people in the GEDCOM with the last name 'Doe' and prints the result.

.. code-block:: python

	from gedcom.element.individual import IndividualElement
	from gedcom.parser import Parser
	
	# Path to your ".ged" file
	file_path = ''
	
	# Name of your ".ged" file
	file_name = ''
	
	# Initialize the parser
	gedcom_parser = Parser()
	
	# Parse your file
	gedcom_parser.parse_file(file_path + file_name)
	
	root_child_elements = gedcom_parser.get_root_child_elements()
	
	# Iterate through all root child elements
	for element in root_child_elements:
	
	    # Is the "element" an actual "IndividualElement"? (Allows usage of extra functions such as "surname_match" and "get_name".)
	    if isinstance(element, IndividualElement):
	
	        # Get all individuals whose surname matches "Doe"
	        if element.surname_match('Doe'):
	
	            # Unpack the name tuple
	            (first, last) = element.get_name()
	
	            # Print the first and last name of the found individual
	            print(first + " " + last)

Example 2
---------
The second example demonstrates the expanded functionality added with this fork including:

* Search for a person in the GEDCOM matching a criteria

* Get name including suffix and sources

* Get a list of spouses

* Get marriage information including sources

* Get date, place and source for first level individual event other than birth, death or burial

* Get all lines between a person and their ancestor.

.. code-block:: python

	from gedcom.parser import Parser
	from gedcom.element import individual
	
	from gedcom.element.individual import IndividualElement
	
	import gedcom.tags
	
	# Path to your ".ged" file
	file_path = ''
	
	# Name of your ".ged" file
	file_name = ''
	
	# Initialize the parser
	parser = Parser()
	parser.parse_file(file_path + file_name)
	
	# Use criteria to find person.  Only one field is required.  The search returns the first match.  
	criteria = "given_name=[first name]:surname=[last name]:birth=[birth year]:death=[death year]"
	individual = parser.find_person(criteria)
	
	if individual == "":
	    print('Person not found')
	    exit()
	
	# Print found person's name and sources for the name.  
	given_name, last_name, suffix, sources = individual.get_name_data()
	print(given_name, last_name, suffix)
	print("\nName Sources:")
	x = 0
	for source in sources:
	    x += 1
	    source_data = parser.get_element_dictionary()[source.get_value()]
	    print(str(x), source_data.get_title(), source_data.get_page())
	
	# Print found person's date and place of birth 
	date, place, sources = individual.get_birth_data()
	print("\nBorn", date, "in", place)
	
	# Print found person's date and place of birth 
	date, place, sources = individual.get_death_data()
	print("Died", date, "in", place)
	
	# Print found person's date and place of baptism.  While there is methods for some first level 
	# events ('BIRT', "BURI' and 'DEAT'), not all are represented.  This function allows easier access
	# without adding methods.
	date, place, sources = individual.get_event_by_tag(tag='BAPM')
	if len(date) > 0 or len(place) > 0:
	    print("Baptized", date, "in", place)
	
	# Print found person's spouse(s) 
	print("\nSpouse(s):")
	for spouse in parser.get_spouses(individual):
	    given_name, last_name, suffix, sources = spouse.get_name_data()    
	    print(given_name, last_name, suffix)
	
	# Print found person's marriage information.  'pointer' is reference to the spouse's pointer.
	# If there is no spouse, the pointer is "".  If you need more information about the spouse,
	# use the element dictionary.
	marriages = parser.get_marriages_data(individual)
	for pointer, date, place, sources in marriages:
	    if len(pointer) > 0:
	        spouse = parser.get_element_dictionary()[pointer]
	        text = "Married {0} {1} on {2} in {3}."
	        print(text.format(spouse.get_first_name(), spouse.get_name()[1], date, place))
	    else:
	        text = "Married unknown person on {0} in {1}."
	        print(text.format(date, place))
	        
	# Print found person's children.
	print("\nChildren:")
	for child in parser.get_children(individual):
	    given_name, surname = child.get_name()
	    print(given_name, surname)
	    
	# Print found person's parents.
	print("\nParents:")
	parents = parser.get_parents(individual)
	for parent in parents:
	    given_name, surname = parent.get_name()
	    print(given_name, surname)
	
	# Print found person's parents from their first parent.
	print("\nGrandparents:")
	grandparents = parser.get_parents(parents[0])
	for grandparent in grandparents:
	    given_name, surname = grandparent.get_name()
	    print(given_name, surname)
	
	# Find path to grandparent.  This is not new.
	print("\nPath to ancestor:")
	lineage = parser.find_path_to_ancestor(individual, grandparents[0], parent_type="ALL")
	text = ""
	
	for line in lineage:
	    given_name, surname, suffix, sources = line.get_name_data()
	    
	    if not line.equals(individual):
	        text += " => "
	    
	    text += (given_name + " " + surname + " " + suffix).strip()
	    
	print(text)
	    
	# Find all paths to one grandparent.  The find_path_to_ancestor method only returns one path.  This function
	# returns all paths,  You would expect only one path to grandparents, but as the generations increase, it is  
	# more likely a person has more than one line
	print("\nPath(s) to ancestor:")
	paths = parser.find_all_paths_to_ancestor(individual, grandparents[0], parent_type="ALL")
	
	x = 0
	while x < len(paths):
	    text = str(x + 1) + " "
	    for line in paths[x]:
	        x += 1
	        given_name, surname, suffix, sources = line.get_name_data()
	        
	        if not line.equals(individual):
	            text += " => "
	        
	        text += (given_name + " " + surname + " " + suffix).strip()
	    
	    print(text)
	    x += 1
