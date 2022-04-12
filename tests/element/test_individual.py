from gedcom.element.element import Element
from gedcom.element.individual import IndividualElement
import gedcom.tags
from gedcom.parser import Parser

def test_initialization():
    individual_element = IndividualElement(level=-1, pointer="", tag=gedcom.tags.GEDCOM_TAG_INDIVIDUAL, value="")
    assert isinstance(individual_element, Element)
    assert isinstance(individual_element, IndividualElement)


def test_get_all_names():
    element = IndividualElement(level=0, pointer="@I5@", tag="INDI", value="")
    element.new_child_element(tag="NAME", value="First /Last/")
    element.new_child_element(tag="SEX", value="M")
    birth = element.new_child_element(tag="BIRT", value="")
    birth.new_child_element(tag="DATE", value="1 JAN 1900")
    element.new_child_element(tag="NAME", value="Second /Surname/")

    all_names = element.get_all_names()
    assert len(all_names) == 2

def test_is_deceased():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:name=Lydia:birth=1939"
    individual = parser.find_person(criteria)
    
    assert individual.is_deceased() == False
    
    criteria = "surname=Coolidge:name=Cynthia:birth=1933"
    individual = parser.find_person(criteria)
    
    assert individual.is_deceased() == True
    
def test_get_name_data():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)
    
    assert individual.get_name_data()[0] == 'John Calvin'
    assert individual.get_name_data()[1] == 'Coolidge'
    assert individual.get_name_data()[2] == 'II'
    
    sources = individual.get_name_data()[3]
    assert len(sources) == 1

    criteria = "surname=Coolidge:birth=1908"
    individual = parser.find_person(criteria)

    assert individual.get_name_data()[0] == 'Calvin'
    assert individual.get_name_data()[1] == 'Coolidge'
    assert individual.get_name_data()[2] == 'Jr.'

    sources = individual.get_name_data()[3]
    assert len(sources) == 0

    criteria = "surname=Trumbull:birth=1904"
    individual = parser.find_person(criteria)
    
    assert individual.get_name_data()[0] == 'Florence'
    assert individual.get_name_data()[1] == 'Trumbull'
    assert individual.get_name_data()[2] == ''

    sources = individual.get_name_data()[3]
    assert len(sources) == 4
    assert sources[0].get_value() == '@S19@'
    assert sources[1].get_value() == '@S14@'
    assert sources[2].get_value() == '@S11@'
    assert sources[3].get_value() == '@S19@'
    
def test_get_first_name():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)
    
    assert individual.get_first_name() == 'John'

    criteria = "surname=Coolidge:birth=1908"
    individual = parser.find_person(criteria)
    
    assert individual.get_first_name() == 'Calvin'

def test_get_birth_date_data():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)
    
    assert individual.get_birth_data()[0] == '4 JUL 1872'
    assert individual.get_birth_data()[1] == 'Plymouth, Windsor, Vermont, USA'
    
    sources = individual.get_birth_data()[2]
    assert len(sources) == 0

    criteria = "surname=Coolidge:birth=1908"
    individual = parser.find_person(criteria)
    
    assert individual.get_birth_data()[0] == '13 APR 1908'
    assert individual.get_birth_data()[1] == 'Northampton, Hampshire, Massachusetts, USA'
    
    sources = individual.get_birth_data()[2]
    assert len(sources) == 2
    assert sources[0].get_value() == '@S17@'
    assert sources[1].get_value() == '@S18@'

def test_get_birth_year():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:death=1933"
    individual = parser.find_person(criteria)
    
    assert individual.get_birth_year() == 1872

    criteria = "surname=Coolidge:death=1924"
    individual = parser.find_person(criteria)
    
    assert individual.get_birth_year() == 1908

def test_get_death_date_data():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Bailey:birth=1909"
    individual = parser.find_person(criteria)
    
    assert individual.get_death_data()[0] == ''
    assert individual.get_death_data()[1] == ''
    
    sources = individual.get_death_data()[2]
    assert len(sources) == 0

    criteria = "surname=Coolidge:death=1924"
    individual = parser.find_person(criteria)
    
    assert individual.get_death_data()[0] == '7 JUL 1924'
    assert individual.get_death_data()[1] == 'District of Columbia, USA'
    
    sources = individual.get_death_data()[2]
    assert len(sources) == 1
    assert sources[0].get_value() == '@S17@'

def test_get_death_year():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Bailey:birth=1909"
    individual = parser.find_person(criteria)
    
    assert individual.get_death_year() == -1

    criteria = "surname=Coolidge:birth=1908"
    individual = parser.find_person(criteria)
    
    assert individual.get_death_year() == 1924

def test_get_burial_data():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:death=1924"
    individual = parser.find_person(criteria)
    
    assert individual.get_burial_data()[0] == '10 JUL 1924'
    assert individual.get_burial_data()[1] == 'Plymouth, Windsor, Vermont, USA'
    
    sources = individual.get_burial_data()[2]
    assert len(sources) == 1
    assert sources[0].get_value() == '@S17@'

    criteria = "surname=Brewer:given_name=Sarah Almeda:death=1906"
    individual = parser.find_person(criteria)
    
    assert individual.get_burial_data()[0] == ''
    assert individual.get_burial_data()[1] == 'Plymouth Notch Cemetery, Plymouth, Windsor, Vermont, USA'
    
    sources = individual.get_burial_data()[2]
    assert len(sources) == 1
    assert sources[0].get_value() == '@S11@'

def test_get_sources_by_tag_and_values():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')
    
    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)
    
    sources = individual.get_sources_by_tag_and_values('BIRT', 'ABT 1873', 'Vermont, USA')
    
    assert len(sources) == 4
    assert sources[0].get_value() == '@S14@'
    assert sources[1].get_value() == '@S1@'
    assert sources[2].get_value() == '@S2@'
    assert sources[3].get_value() == '@S13@'

    sources = individual.get_sources_by_tag_and_values('BIRT', None, 'Vermont, USA')
    
    assert len(sources) == 6

    criteria = "given_name=Florence"
    individual = parser.find_person(criteria)
    
    sources = individual.get_sources_by_tag_and_values('DEAT', '15 FEB 1998', None)
    
    assert len(sources) == 2
    assert sources[0].get_value() == '@S15@'
    assert sources[1].get_value() == '@S11@'
