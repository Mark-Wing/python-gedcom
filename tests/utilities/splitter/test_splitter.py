from gedcom.element.element import Element
from gedcom.element.family import FamilyElement
from gedcom.element.individual import IndividualElement
from gedcom.element.object import ObjectElement
from gedcom.element.source import SourceElement
from gedcom.element.repository import RepositoryElement
import gedcom.tags
from gedcom.utilities.splitter.splitter import Splitter

def test_get_split_gedcom():

    parser = Splitter()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:birth=1816"
    individual = parser.find_person(criteria)
    
    parser.split_gedcom(individual)
    
    count_individuals = 0
    count_sources = 0
    count_repositories = 0
    count_families = 0
    count_objects = 0
        
    for element in parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            count_individuals += 1
        elif isinstance(element, FamilyElement):
            count_families += 1
        elif isinstance(element, SourceElement):
            count_sources += 1
        elif isinstance(element, RepositoryElement):
            count_repositories += 1
        elif isinstance(element, ObjectElement):
            count_objects += 1
        
    assert(count_individuals) == 20
    assert(count_families) == 8
    assert(count_sources) == 18
    assert(count_repositories) == 1
    assert(count_objects) == 28


