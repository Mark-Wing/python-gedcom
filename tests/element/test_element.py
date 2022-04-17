from gedcom.element.element import Element
from gedcom.parser import Parser


def test_initialization():
    element = Element(level=-1, pointer="", tag="", value="")
    assert isinstance(element, Element)


def test_get_sources_by_value():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    source = ""

    for element in parser.get_root_child_elements():
        if element.get_pointer() == '@S1@':
            source = element

    assert source.get_child_value_by_tag('PUBL') == 'Name: Ancestry.com Operations, Inc.; Location: Provo, UT, USA; Date: 2010;'


def test_get_child_value_by_tag():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    obj = parser.get_element_dictionary()['@M20@']
    file = obj.get_child_elements()[0]
    text = file.get_child_value_by_tag("_TEXT")

    assert(text) == "New England Historic Genealogical Society; Boston, Massachusetts; State of Vermont. Vermont Vital Records, 1871–1908"
