import re as regex
import sys, getopt
from pathlib import Path

from gedcom.element.family import FamilyElement
from gedcom.element.individual import IndividualElement
from gedcom.element.individual import NotAnActualIndividualError
from gedcom.element.object import ObjectElement
from gedcom.element.source import SourceElement
from gedcom.element.repository import RepositoryElement
from gedcom.parser import Parser

import gedcom.tags

class Splitter(Parser):
        
    def __init__(self):
        super().__init__()

    def split_gedcom(self, ancestor, include_inlaws=True, callback=None):
        """ Creates a GEDCOM for the a portion of the tree based on the ancester, their
        descendants, their descendants' spouses and their descendants' parents (assuming they
        are not a spouse). If include_inlaws is True, it also includes the parents of spouses and 
        descendants' parents. 
        
        :type ancestor: Element

        :type include_inlaws: bool

        :type callback: function(str message, progress int, progress_total int

        :rtype: str
        """
        
        #validate ancestor
        if not isinstance(ancestor, IndividualElement):
            raise NotAnActualIndividualError(
                "Operation only valid for elements with %s tag" % gedcom.tags.GEDCOM_TAG_INDIVIDUAL
            )
        
        if ancestor.get_pointer() not in self.get_element_dictionary():
            return 'Ancestor not in tree'
        
        #initialize arrays used when determining what to include
        individual_ids = []
        family_ids = []
        source_ids = []
        repository_ids = []
        object_ids = []
        spouses = []
        
        root_elements = len(self.get_root_child_elements())
        people_in_tree = 0
        
        # get descendants, their family elements and the pointers for the their spouses
        count = 0
        for element in self.get_root_child_elements():
            if isinstance(element, IndividualElement):
                people_in_tree += 1
                if self.find_path_to_ancestor(element, ancestor, parent_type="All") != None:
                    individual_ids.append(element.get_pointer())
                    
                    for family_element in self.get_families(element):
                        family_ids.append(family_element.get_pointer())
                        
                        for spouse_element in self.get_family_members(family_element, "PARENTS"):
                            if element.get_pointer() != spouse_element.get_pointer():
                                spouses.append(spouse_element.get_pointer())                        
                
            count += 1
            self.__update_progress("Gathering descendants", count, root_elements, callback)
        
        # get spouses, their family elements and optionally their parents
        count = 0
        for element in self.get_root_child_elements():
            if isinstance(element, IndividualElement):
                if element.get_pointer() in spouses:
                    if element.get_pointer() not in individual_ids: 
                        individual_ids.append(element.get_pointer())
                    
                    for family_element in self.get_families(element, gedcom.tags.GEDCOM_TAG_FAMILY_CHILD):
                        family_ids.append(family_element.get_pointer())
                        
                        if include_inlaws:
                            for parent_element in self.get_parents(element):
                                if parent_element.get_pointer() not in individual_ids:
                                    individual_ids.append(parent_element.get_pointer())

            count += 1
            self.__update_progress("Gathering spouses of descendants", count, root_elements, callback)

        # remove people not in tree
        people_to_remove = people_in_tree - len(individual_ids)        
        count = 0
        x = 0
        while x < len(self.get_root_child_elements()):
            element = self.get_root_child_elements()[x]
            if isinstance(element, IndividualElement):
                if element.get_pointer() not in individual_ids:
                    self.__remove_root_child_element(element)
                    count += 1
                    self.__update_progress("Removing non-family members", count, people_to_remove, callback)
                else:
                    x += 1
            elif isinstance(element, FamilyElement):
                if element.get_pointer() not in family_ids:
                    self.__remove_root_child_element(element)
                else:
                    x += 1
            else:
                x += 1

        # determine which sources are still needed
        root_elements = len(self.get_root_child_elements())
        count = 0
        sources_in_tree = 0
        for element in self.get_root_child_elements():
            if isinstance(element, IndividualElement):
                for child in element.get_child_elements():
                    for childOfChild in child.get_child_elements():
                        if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                            if childOfChild.get_value() not in source_ids:
                                source_ids.append(childOfChild.get_value())

            elif isinstance(element, FamilyElement):
                for child in element.get_child_elements():
                    for childOfChild in child.get_child_elements():
                        if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                            if childOfChild.get_value() not in source_ids:
                                source_ids.append(childOfChild.get_value())
                                
            elif isinstance(element, SourceElement):
                sources_in_tree += 1

            count += 1
            self.__update_progress("Gathering sources", count, root_elements, callback)
                
        # remove sources that are not needed
        sources_to_remove = sources_in_tree - len(source_ids)
        count = 0
        x = 0
        while x < len(self.get_root_child_elements()):
            element = self.get_root_child_elements()[x]
            if isinstance(element, SourceElement):
                if element.get_pointer() not in source_ids:
                    self.__remove_root_child_element(element)
                    count += 1
                    self.__update_progress("Removing unused sources", count, sources_to_remove, callback)
                else:
                    x = x + 1
            else:
                x = x + 1

        # determine which repositories are still needed
        root_elements = len(self.get_root_child_elements())
        count = 0
        repositories_in_tree = 0
        for element in self.get_root_child_elements():
            if isinstance(element, SourceElement):
                repository = element.get_repository()
                if repository != "" and element.get_repository() not in repository_ids:
                    repository_ids.append(element.get_repository())
            elif isinstance(element, RepositoryElement):
                repositories_in_tree += 1
            
            count += 1
            self.__update_progress("Gathering repositories", count, root_elements, callback)
                
        # remove repositories that are not needed
        repositories_to_remove = repositories_in_tree - len(repository_ids)
        count = 0
        x = 0
        while x < len(self.get_root_child_elements()):
            element = self.get_root_child_elements()[x]
            if isinstance(element, RepositoryElement):
                if element.get_pointer() not in repository_ids:
                    self.__remove_root_child_element(element)
                    count += 1
                    self.__update_progress("Removing unused repositories", count, repositories_to_remove, callback)
                else:
                    x = x + 1
            else:
                x = x + 1

        # determine which media objects are still needed
        root_elements = len(self.get_root_child_elements())
        objects_in_tree = 0
        count = 0
        for element in self.get_root_child_elements():
            if isinstance(element, IndividualElement):
                for child in element.get_child_elements():
                    if child.get_tag() == 'OBJE':
                        if child.get_value() not in object_ids:
                            object_ids.append(childOfChild.get_value())

                    else:
                        for childOfChild in child.get_child_elements():
                            if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                                for obj in childOfChild.get_objects():
                                    if obj.get_value() not in object_ids:
                                        object_ids.append(obj.get_value())

            elif isinstance(element, ObjectElement):
                objects_in_tree += 1

            count += 1
            self.__update_progress("Gathering media", count, root_elements, callback)
            
        # remove objects that are not needed
        objects_to_remove = objects_in_tree - len(object_ids)
        count = 0
        x = 0        
        while x < len(self.get_root_child_elements()):
            element = self.get_root_child_elements()[x]
            if isinstance(element, ObjectElement):
                if element.get_pointer() not in object_ids:
                    self.__remove_root_child_element(element)
                    count += 1    
                    self.__update_progress("Removing unused media", count, objects_to_remove, callback)
                else:
                    x = x + 1
            else:
                x = x + 1
 
    def write_file(self, file_name, callback=None):
        """Writes tree in output file

        :type file_name: str
        
        :type callback: function(message as str, count as int, total as int)
        """        
        root_elements = len(self.get_root_child_elements())
        count = 0
        
        f_out = open(file_name , 'w', encoding='utf-8', newline='')
        
        for element in self.get_root_child_elements():
            f_out.write(element.to_gedcom_string(True))
            count += 1
            self.__update_progress("Writing file", count, root_elements, callback)
        f_out.close()      
           
    def __update_progress(self, message, count, total, callback):
        """if there is a callback function, calls the functions"""
        if callback != None:
            callback(message, count, total)
                
    def __remove_root_child_element(self, element):
        """Removes child element from list of root elements                 
        
        :type element: Element
        """
        self.get_root_element().remove_child_element(element.get_pointer())

# functions for support running from command line 
def print_usage_message():

    print('usage: python splitter.py -i <gedcom-input-file> [-h | -b <year-of-birth> | -d <year-of-death> | -g <given-name> | -l <last-name> | -o <gedcom-output-file> | -n] ')
    print('Options and arguments (and corresponding environment variables):')
    print('-b : root person\'s year of birth')
    print('-d : root person\'s year of death')
    print('-g : part of all of the root person\'s given name')
    print('-h : print this help message and exit')
    print('-i : file name of the source GEDCOM file')
    print('-l : part of all of the root person\'s last name')
    print('-n : exclude father-in-law and mother-in-law of descendants')
    print('-o : file name of output GEDCOM file; if not included, adds "_split" to the input file name')
    print('-s : does not enforce strict parsing of GEDCOM file')

def build_criteria(criteria, field, value):

    if value != "":
        if criteria != "":
            criteria += ":"

        criteria += field + "=" + value
    
    return criteria

def progress_status(message, progress, progress_total):

    barLength = 30 # Modify this to change the length of the progress bar
    #status = ""
    #if isinstance(progress, int):
    #    progress = float(progress)

    if progress == 1:
        print()
        
    percent = round(progress / progress_total, 3)

    block = int(round(barLength * percent))
    #percent = round(progress*100, 3)
    
    text = "\r{0}: [{1}] {2}/{3}                  ".format( message, "#"*block + "-"*(barLength-block), progress, progress_total)
    sys.stdout.write(text)
    sys.stdout.flush()

        
def main(argv):
   
    input_file = ''
    output_file = ''
    include_inlaws = True
    birth_year = ""
    death_year = ""
    given_name = ""
    last_name = ""
    strict = True
   
    try:
        opts, args = getopt.getopt(argv,"b:d:g:h:i:l:n:o:s")
   
        for opt, arg in opts:
            if opt == '-h':
                print_usage_message()
                sys.exit()
            elif opt in ("-b"):
                birth_year = arg
            elif opt in ("-d"):
                death_year = arg
            elif opt in ("-i"):
                input_file = arg
            elif opt in ("-g"):
                given_name = arg
            elif opt in ("-l"):
                last_name = arg
            elif opt in ("-n"):
                include_inlaws = False
            elif opt in ("-o"):
                output_file = arg
            elif opt in ("-s"):
                strict = False
                
        if not Path(input_file).is_file():
            print("Input file is not a valid file")
            print_usage_message()
            sys.exit()

        if output_file == "":
            output_file = str(Path(input_file).parent)  + "/" + str(Path(input_file).stem) \
                            + "_split" + str(Path(input_file).suffix)
        elif not Path(input_file).is_file():
            print("Output file is not a valid file")
            print_usage_message()
            sys.exit()
        
        criteria = ""
        
        criteria = build_criteria(criteria, 'given_name', given_name)
        criteria = build_criteria(criteria, 'surname', last_name)
        criteria = build_criteria(criteria, 'birth', birth_year)
        criteria = build_criteria(criteria, 'death', death_year)

        if criteria == "":
            print('The root ancestor must be identied by at least one of the following fields:')
            print('* birth year')
            print('* death year')
            print('* given_name')
            print('* last name')
            print_usage_message()
            sys.exit()
            
        parser = Splitter()
        parser.parse_file(input_file, strict=strict, callback=progress_status)
        
        ancestor = parser.find_person(criteria)
        
        if ancestor == "":
            print("No ancestor was found")
        else:
            parser.split_gedcom(ancestor, include_inlaws=include_inlaws, callback=progress_status)
            parser.write_file(output_file, callback=progress_status)
            print("\nSplit complete")
      
    except getopt.GetoptError:
        print_usage_message()
   
if __name__ == "__main__":
    main(sys.argv[1:])    
    
    
    