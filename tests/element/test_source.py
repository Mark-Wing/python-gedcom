from gedcom.element.source import SourceElement
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser


def test_initialization():

    element = SourceElement(level=-1, pointer="", tag="", value="")
    assert isinstance(element, SourceElement)


def test_getters():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    source = ""

    for element in parser.get_root_child_elements():
        if element.get_pointer() == '@S1@':
            source = element

    assert source.get_author() == 'Ancestry.com'
    assert source.get_page() == ''
    assert source.get_publisher() == 'Name: Ancestry.com Operations, Inc.; Location: Provo, UT, USA; Date: 2010;'
    assert source.get_repository() == '@R1@'
    assert source.get_title() == '1920 United States Federal Census'

    person = "surname=Coolidge:birth=1872"
    individual = ""

    for element in parser.get_root_child_elements():
        if isinstance(element, IndividualElement):
            if element.criteria_match(person):
                individual = element

    sources = individual.get_name_data()[3]

    assert sources[0].get_page() == 'Year: 1910; Census Place: Northampton Ward 2, Hampshire, Massachusetts; Roll: T624_593; Page: 1B; Enumeration District: 0696; FHL microfilm: 1374606'
    assert len(sources[0].get_objects()) == 1
