from gedcom.element.element import Element
from gedcom.element.family import FamilyElement
import gedcom.tags
from gedcom.parser import Parser

def test_initialization():
    family_element = FamilyElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_FAMILY, value="")
    assert isinstance(family_element, Element)
    assert isinstance(family_element, FamilyElement)
    
def test_get_children():
    
    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)

    families = parser.get_families(individual)

    children = families[0].get_children()
    
    assert(children[0].get_value() == '@I20@')
    assert(children[1].get_value() == '@I21@')
        
def test_get_husbands():
    
    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)

    families = parser.get_families(individual)
    
    husbands = families[0].get_husbands()
    
    assert(husbands[0].get_value() == '@I16@')
    
def test_get_wives():
    
    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)

    families = parser.get_families(individual)
    
    wives = families[0].get_wives()
    
    assert(wives[0].get_value() == '@I19@')

def test_get_marriages():
    
    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1845"
    individual = parser.find_person(criteria)

    families = parser.get_families(individual)
    
    marriages = families[0].get_marriages()
    
    assert(marriages[0].get_child_value_by_tag('DATE') == '6 MAY 1868')
    assert(marriages[0].get_child_value_by_tag('PLAC') == 'Plymouth, Windsor, Vermont, USA')

def test_get_marriages_data():
    
    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1845"
    individual = parser.find_person(criteria)

    families = parser.get_families(individual)
    
    marriages = families[0].get_marriages_data()
    
    date, place, source = marriages[0]
    
    assert(date == '6 MAY 1868')
    assert(place == 'Plymouth, Windsor, Vermont, USA')