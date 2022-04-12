from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement

import gedcom.tags

import os
from gedcom.element import individual

file_path = os.path.dirname(os.path.realpath(__file__))
file_name = '/files/Coolidge.ged'
    
parser = Parser()
parser.parse_file(file_path + file_name)

# Use criteria to find person.  Only one field is required.  The search returns the first match   
criteria = "given_name=[first name]:surname=[last name]:birth=[birth year]:death=[death year]"
criteria = "surname=Coolidge:birth=1872"
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
# events ('BIRT', "BURI' and 'DEAT'), not all are represented.  This function allows easier access.
date, place, sources = individual.get_event_by_tag(tag='BAPM')
if len(date) > 0 or len(place) > 0:
    print("Baptized", date, "in", place)

# Print found person's spouse(s) 
print("\nSpouse(s):")
for spouse in parser.get_spouses(individual):
    given_name, last_name, suffix, sources = spouse.get_name_data()    
    print(given_name, last_name, suffix)

# Print found person's marriage information.  Pointer reference to the spouse's pointer.
# If there is no spouse, the pointer is "".  If you need more information about the spouse,
# use the element dictionary
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
    
# Find all paths to grandparent.  The find_path_to_ancestor method only returns one path.  This function
# returns all paths,  You would expect one path to grandparents, but as the generations increase, this 
# becomes more likely 
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