from gedcom.element.individual import IndividualElement
from gedcom.element.root import RootElement
from gedcom.parser import Parser


def test_initialization():
    parser = Parser()
    assert isinstance(parser, Parser)


def test_invalidate_cache():

    parser = Parser()
    parser.parse_file('tests/files/Musterstammbaum.ged')

    assert len(parser.get_element_list()) == 396
    assert len(parser.get_element_dictionary()) == 32

    parser.invalidate_cache()

    assert len(parser.get_element_list()) == 396
    assert len(parser.get_element_dictionary()) == 32


def test_get_root_element():
    parser = Parser()
    assert isinstance(parser.get_root_element(), RootElement)


def test_parse_file():

    parser = Parser()

    assert len(parser.get_root_child_elements()) == 0

    parser.parse_file('tests/files/Musterstammbaum.ged')

    assert len(parser.get_root_child_elements()) == 34

    individuals_in_root_child_elements = 0
    individuals_in_element_list = 0

    for element in parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            individuals_in_root_child_elements += 1

    for element in parser.get_element_list():
        if isinstance(element, IndividualElement):
            individuals_in_element_list += 1

    assert individuals_in_root_child_elements == 20
    assert individuals_in_element_list == 20


def test_parse_from_string():
    case_1 = """0 @I5@ INDI
1 NAME First /Last/
1 SEX M
1 BIRT
2 DATE 1 JAN 1900
2 PLAC Kirkland, King, Washington, USA
3 MAP
4 LATI N47.680663
4 LONG W122.234319
"""
    gedcom_parser = Parser()
    gedcom_parser.parse([(a + '\n').encode('utf-8-sig') for a in case_1.splitlines()])
    element_1 = gedcom_parser.get_root_child_elements()[0]
    assert isinstance(element_1, IndividualElement)
    assert element_1.get_tag() == 'INDI'
    assert element_1.get_pointer() == '@I5@'
    element_1_children = element_1.get_child_elements()
    assert len(element_1_children) == 3
    assert element_1_children[0].get_tag() == 'NAME'
    assert element_1_children[1].get_tag() == 'SEX'
    assert element_1_children[2].get_tag() == 'BIRT'

    case_2 = """0 @F28@ FAM
1 HUSB @I80@
1 WIFE @I81@
1 CHIL @I9@
2 _FREL Natural
2 _MREL Natural
1 CHIL @I84@
2 _FREL Natural
2 _MREL Natural
1 CHIL @I85@
2 _FREL Natural
2 _MREL Natural
"""
    gedcom_parser.parse([(a + '\n').encode('utf-8-sig') for a in case_2.splitlines()])
    element_2 = gedcom_parser.get_root_child_elements()[0]
    assert element_2.get_tag() == 'FAM'
    assert element_2.get_pointer() == '@F28@'
    element_2_children = element_2.get_child_elements()
    assert len(element_2_children) == 5
    assert element_2_children[0].get_tag() == 'HUSB'
    assert element_2_children[1].get_tag() == 'WIFE'
    assert element_2_children[2].get_tag() == 'CHIL'
    assert element_2_children[3].get_value() == '@I84@'


def test___parse_line():
    # @TODO Add appropriate testing cases
    pass


def test_get_marriages():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1845"
    individual = parser.find_person(criteria)

    marriages = parser.get_marriages(individual)

    assert len(marriages) == 2

    assert marriages[0] == ('6 MAY 1868', 'Plymouth, Windsor, Vermont, USA')
    assert marriages[1] == ('9 SEP 1891', 'Plymouth, Litchfield, Vermont, USA')


def test_get_marriages_data():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1845"
    individual = parser.find_person(criteria)

    marriages = parser.get_marriages_data(individual)

    assert len(marriages) == 2

    (spouse, date, place, sources) = marriages[0]

    assert spouse == '@I18@'
    assert date == '6 MAY 1868'
    assert place == 'Plymouth, Windsor, Vermont, USA'

    assert len(sources) == 1
    assert sources[0].get_value() == '@S21@'

    (spouse, date, place, sources) = marriages[1]

    assert spouse == '@I9@'
    assert date == '9 SEP 1891'
    assert place == 'Plymouth, Litchfield, Vermont, USA'

    assert len(sources) == 2
    assert sources[0].get_value() == '@S9@'


def test_get_parents():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)

    parents = parser.get_parents(individual)

    assert len(parents) == 2
    assert parents[0].get_pointer() == '@I17@'
    assert parents[1].get_pointer() == '@I18@'


def test_get_children():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)

    children = parser.get_children(individual)

    assert len(children) == 2
    assert children[0].get_pointer() == '@I20@'
    assert children[1].get_pointer() == '@I21@'


def test_get_spouses():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1845"
    individual = parser.find_person(criteria)

    spouses = parser.get_spouses(individual)

    assert len(spouses) == 2
    assert spouses[0].get_pointer() == '@I18@'
    assert spouses[1].get_pointer() == '@I9@'


def test_get_family():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    criteria = "surname=Coolidge:birth=1872"
    individual = parser.find_person(criteria)

    persons = parser.get_family(individual)

    assert len(persons) == 2
    assert persons[0].get_pointer() == '@I20@'
    assert persons[1].get_pointer() == '@I21@'

    persons = parser.get_family(individual, members_type="ALL")

    assert len(persons) == 4
    assert persons[0].get_pointer() == '@I16@'
    assert persons[1].get_pointer() == '@I19@'
    assert persons[2].get_pointer() == '@I20@'
    assert persons[3].get_pointer() == '@I21@'
