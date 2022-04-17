from gedcom.element.repository import RepositoryElement
from gedcom.parser import Parser


def test_initialization():

    element = RepositoryElement(level=-1, pointer="", tag="", value="")
    assert isinstance(element, RepositoryElement)


def test_getters():

    parser = Parser()
    parser.parse_file('tests/files/Coolidge.ged')

    repository = ""

    for element in parser.get_root_child_elements():
        if element.get_pointer() == '@R1@':
            repository = element

    assert repository.get_name() == 'Ancestry.com'
    assert repository.get_address() == '52-55 Sir John Rogersons Quay, Dublin 2, Ireland'
